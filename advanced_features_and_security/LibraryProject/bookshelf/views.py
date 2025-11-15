from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm, ExampleForm


# ---------- BOOK LIST ----------
# List all books - permission required: can_view
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()  # Safe ORM query
    return render(request, 'bookshelf/book_list.html', {'books': books})


# ---------- CREATE BOOK ----------
# Create a new book - permission required: can_create
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.added_by = request.user  # Secure assignment
            new_book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})


# ---------- EDIT BOOK ----------
# Edit an existing book - permission required: can_edit
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Safe from injection
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})


# ---------- DELETE BOOK ----------
# Delete a book - permission required: can_delete
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Safe ORM query
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


# ---------- EXAMPLE FORM VIEW ----------
def example_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # No DB operations → completely safe
            return render(request, 'bookshelf/form_success.html')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

