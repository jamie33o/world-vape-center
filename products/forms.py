from django import forms
from .models import Review
from .models import Brand, ProductVariant
from collections import defaultdict


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
    """

    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        to_field_name='slug'
    )

    variants = forms.ModelMultipleChoiceField(
        queryset=ProductVariant.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        to_field_name='id'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Group variants by their type
        grouped_variants = defaultdict(list)
        for variant in ProductVariant.objects.all():
            grouped_variants[variant.variant_type].append((variant.id, variant.name))

        # Store grouped variants as choices in a dictionary
        self.grouped_variants = dict(grouped_variants)
