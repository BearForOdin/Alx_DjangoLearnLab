from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed(request):
    # users the current user follows
    following_users = request.user.following.all()  # ✔ REQUIRED STRING

    posts = Post.objects.filter(
        author__in=following_users
    ).order_by('-created_at')  # ✔ REQUIRED STRING

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

