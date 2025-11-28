from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# List all books
class BookListView(generics.ListAPIView):
    """
    Retrieves all Book instances.
    Accessible to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single Book instance by primary key.
    Accessible to all users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Create a new book
class BookCreateView(generics.CreateAPIView):
    """
    Allows authenticated users to create a new Book.
    Validates publication_year before saving.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Update an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    Allows authenticated users to update an existing Book.
    Validates publication_year before saving.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    """
    Allows authenticated users to delete a Book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
