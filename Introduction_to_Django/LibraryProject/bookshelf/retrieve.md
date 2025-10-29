
---

### 📄 `retrieve.md`
```markdown
# Retrieve Operation

```python
from bookshelf.models import Book

# Retrieve all books
books = Book.objects.all()
print(books)

# Retrieve the first book and print its details
b = Book.objects.first()
print(b.title)
print(b.author)
print(b.publication_year)
