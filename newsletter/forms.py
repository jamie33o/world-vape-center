# in forms.py
from django import forms

class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(label='Email:')
