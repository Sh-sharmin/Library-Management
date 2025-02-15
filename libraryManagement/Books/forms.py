from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Review '}),
        }