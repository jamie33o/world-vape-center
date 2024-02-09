from django import forms
from .models import MultiOption
from .models import Brand


class AdminAddMultiOptionForm(forms.Form):
    ids = forms.CharField(widget=forms.HiddenInput, required=False)
    options_name = forms.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        multi_option_data = MultiOption.objects.all()
        choices_list = [(option.id, option.name) for option in multi_option_data]

        self.fields['choices'] = forms.MultipleChoiceField(
            choices=choices_list,
            widget=forms.CheckboxSelectMultiple,
        )

class AdminAddMultipleBrandsForm(forms.Form):
    ids = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        brands = Brand.objects.all()
        brands_list = [(brand.id, brand.name) for brand in brands]

        self.fields['brand'] = forms.ChoiceField(
            choices=brands_list,
            widget=forms.RadioSelect,
        )


class AdminAddPricesForm(forms.Form):
    ids = forms.CharField(widget=forms.HiddenInput, required=False)
    price = forms.DecimalField(label='Price', required=True, min_value=0.01)
