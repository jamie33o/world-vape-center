from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_GET
from django.contrib import messages
from world_vape_center.urls import sitemaps
from .forms import ContactForm

@require_GET
def payments_options(request):
    return render(request, 'help/payment-options.html')

@require_GET
def delivery_info(request):
    return render(request, 'help/delivery-info.html')

@require_GET
def about_us(request):
    return render(request, 'help/about-us.html')

@require_GET
def returns_policy(request):
    return render(request, 'help/returns-policy.html')

@require_GET
def terms(request):
    return render(request, 'help/terms.html')

@require_GET
def faq(request):
    return render(request, 'help/faq.html')

@require_GET
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

@require_GET
def sitemap_html(request):
    urls = {}

    for key, value in sitemaps.items():
        sitemap_class = value()
        sitemap_urls = sitemap_class.get_urls()
        urls[key] = [url['location'] for url in sitemap_urls]

    return render(request, 'help/sitemap.html', {'urls': urls})
