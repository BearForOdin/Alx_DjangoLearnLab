
---

### 📄 `update.md`
```markdown
# Update Operation

```python
from bookshelf.models import Book

# Retrieve and update the book title
b = Book.objects.get(title="1984")
b.title = "Nineteen Eighty-Four"
b.save()

# Confirm the update
print(b)
print(Book.objects.get(pk=b.pk).title)
