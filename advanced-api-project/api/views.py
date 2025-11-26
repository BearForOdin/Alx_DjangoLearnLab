from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

"""
BookListView
-------------
Handles GET requests to list all Book objects.
Allows unauthenticated users to read data.
"""
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


"""
BookDetailView
---------------
Handles GET requests for a single Book object identified by its PK.
Allows unauthenticated users to read data.
"""
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


"""
BookCreateView
---------------
Handles POST requests to create new Book objects.
Requires the user to be authenticated.
Includes automatic serializer validation.
"""
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Optional: Modify behavior before saving
    def perform_create(self, serializer):
        # Example: log the user or attach metadata
        print(f"Book created by: {self.request.user}")
        serializer.save()


"""
BookUpdateView
---------------
Handles PUT/PATCH to modify an existing Book.
Requires authentication.
Runs serializer validation automatically.
"""
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Optional: Validate or customize update behavior
    def perform_update(self, serializer):
        print(f"Book updated by: {self.request.user}")
        serializer.save()


"""
BookDeleteView
---------------
Handles DELETE requests to remove a Book.
Requires authentication.
"""
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
