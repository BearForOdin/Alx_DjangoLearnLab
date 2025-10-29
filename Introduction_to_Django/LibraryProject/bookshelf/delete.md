
---

### 📄 `delete.md`
```markdown
# Delete Operation

```python
from bookshelf.models import Book

# Retrieve and delete the book
b = Book.objects.get(title="Nineteen Eighty-Four")
b.delete()

# Confirm deletion
print(Book.objects.all())
