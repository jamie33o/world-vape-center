from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm


def payments_options(request):
    return render(request, 'help/payment-options.html')

def delivery_info(request):
    return render(request, 'help/delivery-info.html')

def about_us(request):
    return render(request, 'help/about-us.html')

def returns_policy(request):
    return render(request, 'help/returns-policy.html')

def terms(request):
    return render(request, 'help/terms.html')

def faq(request):
    return render(request, 'help/faq.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save form data to variables
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            subject = 'New Contact Form Submission'
            message_body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
            sender_email = email
            recipient_email = settings.DEFAULT_FROM_EMAIL 

            send_mail(subject, message_body, sender_email, [recipient_email])
            messages.success(request, 'Your message has been sent successfully!')  # Add success message

            return redirect('contact_us')
    else:
        form = ContactForm()

    return render(request, 'help/contact-us.html', {'form': form})
