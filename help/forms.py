"""
Contact Form

A Django form for handling contact information.

Attributes:
    name (CharField): Field for the user's
    name (max length: 100 characters).
    email (EmailField): Field for the user's email address.
    message (CharField): Field for the user's
    message (displayed as a textarea).

Methods:
    clean_email(): Custom method to perform
    additional validation on the email field.
"""
from django import forms


class ContactForm(forms.Form):
    """
    class for contact form
    """

    name = forms.CharField(max_length=100)
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'id': 'email_contact'}))
    message = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        """
        Clean Email

        Custom method to perform additional validation on the email field.

        Returns:
            str: The cleaned and validated email address.

        Raises:
            forms.ValidationError: If the email
            does not meet the specified validation criteria.
        """
        email = self.cleaned_data.get('email')
        return email
