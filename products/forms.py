from django import forms
from .models import Review, MultiOption
from .models import Brand


class ReviewForm(forms.ModelForm):
    """
    Form for adding or updating a product review.

    Meta:
    - model (Review): The model associated with the form.
    - fields (list): The fields to include in the form.

    Widgets:
    - name (TextInput): Text input widget for the name field.
    - rating (NumberInput): Number input widget for the rating field.
    - comment (Textarea): Textarea widget for the comment field.

    """
    class Meta:
        model = Review
        fields = ['name', 'rating', 'comment']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'rating': forms.NumberInput(attrs={'class': 'form-control',
                                           'min': 0,
                                           'max': 5, 'step': 1}),
        'comment': forms.Textarea(attrs={'class': 'form-control'}),
    }


class FiltersForm(forms.Form):
    """
    Form for applying filters to product listings.

    Attributes:
    - brands (ModelMultipleChoiceField):
    Multiple choice field for brands.
    - multi_options (ModelMultipleChoiceField):
    Multiple choice field for multi-options.

    """
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
