from django import forms

class AddToCartForm(forms.Form):
    """
    Form for adding a product to the shopping cart.

    Attributes:
        options (forms.ChoiceField): A radio select field for product options.
        product_quantity (forms.ChoiceField): A select field for choosing the quantity.
        product_id (forms.IntegerField): A hidden input field for storing the product ID.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the form with the specified product details.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Keyword Args:
            product_id (int): The ID of the product.
            product_option_name (str): The name of the product option.
            product_options (list): List of product options.

        """
        product_id = kwargs.pop('product_id', None)
        product_option_name = kwargs.pop('product_option_name', None)
        product_options = kwargs.pop('product_options', [])
        super(AddToCartForm, self).__init__(*args, **kwargs)

        if product_options:
            self.fields['options'] = forms.ChoiceField(
                label=product_option_name,
                widget=forms.RadioSelect,
                choices=[(option.name, option.name) for option in product_options],
                required=False,
                initial=product_options[0].name if product_options else None,
            )

        self.fields['product_quantity'] = forms.ChoiceField(
            choices=[(str(i), str(i)) for i in range(1, 9)],
            widget=forms.Select(attrs={'class': 'form-select form-select-sm form-qty'}),
            initial='1',
        )

        self.fields['product_id'] = forms.IntegerField(
            widget=forms.HiddenInput(),
            initial=product_id,
        )

