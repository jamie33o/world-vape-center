from django import forms
from .models import Review, MultiOption
from .models import Brand

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 5, 'step': 1}),
        'comment': forms.Textarea(attrs={'class': 'form-control'}),
    }


class FiltersForm(forms.Form):
    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        to_field_name='slug'
    )

    multi_options = forms.ModelMultipleChoiceField(
        queryset=MultiOption.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        to_field_name='slug'
    )

