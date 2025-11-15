from django import forms
from .models import Book

# Form for Book model
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if "<script>" in title.lower():
            raise forms.ValidationError("Invalid characters in title!")
        return title


# Example form to satisfy requirement
class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    # Optional extra validation
    def clean_message(self):
        msg = self.cleaned_data.get('message')
        if "<script>" in msg.lower():
            raise forms.ValidationError("Invalid characters in message!")
        return msg
