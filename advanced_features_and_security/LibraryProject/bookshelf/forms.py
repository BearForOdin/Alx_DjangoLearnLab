from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']  # Only allow these fields

    # Optional: extra validation example
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if "<script>" in title.lower():
            raise forms.ValidationError("Invalid characters in title!")
        return title
