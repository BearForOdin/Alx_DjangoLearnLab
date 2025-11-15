# Retrieve Operation

```python
from bookshelf.models import Book

# Retrieve the book with the title "1984"
b = Book.objects.get(title="1984")

# Display the book details
print(b.title)
print(b.author)
print(b.publication_year)
