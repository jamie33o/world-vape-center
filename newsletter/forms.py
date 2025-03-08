from django import forms

class NewsletterSubscriptionForm(forms.Form):
    """
    Newsletter Subscription Form

    A simple form for capturing email
    addresses for newsletter subscriptions.
    """

    email = forms.EmailField(
        label="Email:",
        widget=forms.EmailInput(
            attrs={
                "id": "email_newsletter",
                "class": "w-full text-black border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500",
                "placeholder": "Enter your email",
            }
        ),
    )
