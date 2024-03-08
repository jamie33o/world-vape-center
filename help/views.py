from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_GET
from django.contrib import messages
from world_vape_center.urls import sitemaps
from products.models import Category
from .forms import ContactForm


@require_GET
def payments_options(request):
    """
    Render the payment options page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered payment options page.
    """
    return render(request, 'help/payment-options.html')


@require_GET
def delivery_info(request):
    """
    Render the delivery information page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered delivery information page.
    """
    return render(request, 'help/delivery-info.html')


@require_GET
def about_us(request):
    """
    Render the about us page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered about us page.
    """
    return render(request, 'help/about-us.html')


@require_GET
def returns_policy(request):
    """
    Render the returns policy page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered returns policy page.
    """
    return render(request, 'help/returns-policy.html')


@require_GET
def terms(request):
    """
    Render the terms page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered terms page.
    """
    return render(request, 'help/terms.html')


@require_GET
def faq(request):
    """
    Render the FAQ page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered FAQ page.
    """
    return render(request, 'help/faq.html')

@require_GET
def privacy_policy(request):
    """
    Render the cookie policy page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered cookie policy page.
    """
    return render(request, 'help/privacy-policy.html')

@require_GET
def contact_us(request):
    """
    Render the contact us page and handle contact form submissions.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered contact us page.
    """
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
            messages.success(request,
                             'Your message has been sent successfully!')

            return redirect('contact_us')
    else:
        form = ContactForm()

    return render(request, 'help/contact-us.html', {'form': form})


@require_GET
def sitemap_html(request):
    """
    Render the HTML sitemap page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered sitemap page.
    """
    urls = {}

    for key, value in sitemaps.items():
        sitemap_class = value()
        sitemap_urls = sitemap_class.get_urls()
        urls[key] = []
        for sitemap_item in sitemap_urls:
            urls[key].append((
                sitemap_item['item'],
                sitemap_item['location']
            ))
    categories = Category.objects.all()

    context = {'urls': urls,
               'categories': categories}
    return render(request, 'help/sitemap.html', context)
