from django import forms
from .models import Review, MultiOption
from .models import Brand, MultiOption

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
    ids = forms.CharField()
    options_name = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        multi_option_data = MultiOption.objects.all()
        choices_list = [(option.id, option.name) for option in multi_option_data]

        self.fields['choices'] = forms.MultipleChoiceField(
            choices=choices_list,
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )


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

