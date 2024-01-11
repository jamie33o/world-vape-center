from django import forms
from .models import Review, MultiOption
import json
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate choices dynamically from MultiOption JSONField key-value pairs
        multi_option_data = MultiOption.objects.all().values('id', 'options')
        choices_list = []

        for option_data in multi_option_data:
            try:
                key = list(option_data['options'].keys())[0]
                value = option_data['options'][key]
                label = f"{key}: {value}"
                choices_list.append((option_data['id'], label))
            except (json.JSONDecodeError, AttributeError, IndexError):
                pass

        self.fields['choices'] = forms.MultipleChoiceField(
            choices=choices_list,
            widget=forms.RadioSelect,
            required=False,
        )
