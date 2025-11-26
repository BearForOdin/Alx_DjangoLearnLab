from django.db import models
from django.utils import timezone

"""
Author Model:
- Represents a book author.
- Holds only a 'name' field.
"""
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


"""
Book Model:
- Represents a book written by an author.
- Linked to Author through a ForeignKey, creating a one-to-many relationship.
"""
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"     # enables nested serialization
    )

    def __str__(self):
        return self.title

