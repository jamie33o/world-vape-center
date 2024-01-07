from django import forms
from .models import Review, MultiChoice

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5, 'step': 1}),
        'comment': forms.Textarea(attrs={'class': 'form-control'}),
    }

class CustomActionForm(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset=MultiChoice.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    ids = forms.CharField()

