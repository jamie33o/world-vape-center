from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            "class": "w-16 text-center rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
        })
    )

    def __init__(self, *args, product=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = product

        if product and product.has_variants():
            for variant_type, options in product.get_variant_options().items():
                choices = []
                for option in options:
                    # Get stock count for this variant
                    variant = product.variants.filter(variant_type=variant_type, name=option).first()
                    stock_count = variant.countInStock if variant else 0

                    # Format the option with stock count
                    formatted_option = f"{option} ({stock_count} in stock)"
                    choices.append((option, formatted_option))

                self.fields[variant_type] = forms.ChoiceField(
                    choices=choices,
                    required=True,
                    widget=forms.Select(attrs={
                        "class": "w-full p-2 border rounded-md focus:ring focus:ring-blue-200"
                    })
                )
            
