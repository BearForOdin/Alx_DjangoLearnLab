from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from django import forms
from .forms import BookForm  # You’ll need a form for Book

# List all books - permission required: can_view
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


# Create a new book - permission required: can_create
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.added_by = request.user
            new_book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})


# Edit an existing book - permission required: can_edit
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})


# Delete a book - permission required: can_delete
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()  # Safe ORM query
    return render(request, 'bookshelf/book_list.html', {'books': books})