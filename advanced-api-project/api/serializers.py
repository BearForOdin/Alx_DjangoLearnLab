from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

"""
BookSerializer:
- Serializes all fields in Book.
- Includes custom validation to ensure publication_year is not greater than the current year.
"""
class BookSerializer(serializers.ModelSerializer):

    # Custom validation for publication_year
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value

    class Meta:
        model = Book
        fields = '__all__'


"""
AuthorSerializer:
- Serializes the 'name' field.
- Includes nested serialization of related Book objects using BookSerializer.
- Uses 'books' because of related_name="books" in the Book model.
"""
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
