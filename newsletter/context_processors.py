# in your_project/context_processors.py
from .forms import NewsletterSubscriptionForm

def newsletter_form(request):
    return {'newsletter_form': NewsletterSubscriptionForm()}
