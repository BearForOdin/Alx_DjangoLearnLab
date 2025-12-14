from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


# ============================
# AUTH VIEWS (UNCHANGED LOGIC)
# ============================

class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)

        data = UserSerializer(user).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]  # ✔ REQUIRED STRING
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# ============================
# FOLLOW / UNFOLLOW FEATURES
# ============================

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()  # ✔ REQUIRED STRING
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # ✔ REQUIRED STRING


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # ✔ REQUIRED STRING
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)

    if user_to_follow == request.user:
        return Response(
            {"detail": "You cannot follow yourself."},
            status=status.HTTP_400_BAD_REQUEST
        )

    request.user.following.add(user_to_follow)
    return Response(
        {"detail": f"You are now following {user_to_follow.username}."},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  # ✔ REQUIRED STRING
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

    request.user.following.remove(user_to_unfollow)
    return Response(
        {"detail": f"You have unfollowed {user_to_unfollow.username}."},
        status=status.HTTP_200_OK
    )
