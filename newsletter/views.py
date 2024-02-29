"""
Subscribe to Newsletter

Handles the subscription to the newsletter. Accepts POST
requests with a valid email address.
Returns a JSON response indicating success or failure.

Parameters:
    request (HttpRequest): The incoming HTTP request.

Returns:
    JsonResponse: A JSON response indicating the success
    or failure of the subscription.
"""
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from .models import Subscriber
from .forms import NewsletterSubscriptionForm


@require_POST
def subscribe_newsletter(request):
    """
    Unsubscribe from Newsletter

    Handles the unsubscription from the newsletter.
    Accepts POST requests with a valid email address.
    Returns a JSON response indicating success or failure.

    Parameters:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the
        success or failure of the unsubscription.
    """

    form = NewsletterSubscriptionForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']

        try:
            # Create a new Subscriber instance
            subscriber = Subscriber.objects.filter(email=email).first()
            if subscriber:
                # The email exists, remove the subscriber
                email = subscriber.email
                context = {'email': email}

                subscriber.delete()
                email_content = render_to_string('unsub_email.html', context)

                email_subject = 'You have Unsubscribed'
                recipient_list = [email]
                from_email = settings.EMAIL_HOST_USER

                send_mail(
                    email_subject,
                    '',
                    from_email,
                    recipient_list,
                    html_message=email_content,
                    fail_silently=False
                )

                response_data = {
                    'status': 'success',
                    'message':
                    'Successfully un-subscribed from the newsletter.',
                }

                return JsonResponse(response_data)

            # Create a new Subscriber instance
            subscriber = Subscriber(email=email)
            subscriber.full_clean()
            subscriber.save()

            context = {'email': subscriber.email, }
            email_content = render_to_string('sub_thank_you_email.html',
                                             context)

            email_subject = 'Thank you for Subscribing'
            recipient_list = [subscriber.email]
            from_email = settings.EMAIL_HOST_USER

            send_mail(
                email_subject,
                '',
                from_email,
                recipient_list,
                html_message=email_content,
                fail_silently=False
            )
            response_data = {
                'status': 'success',
                'message': 'Successfully subscribed to the newsletter.'
            }
            return JsonResponse(response_data)

        except Exception as e:
            print(e)
            response_data = {
                    'status': 'danger',
                    'message': e
                }
            return JsonResponse(response_data)

    else:
        response_data = {
                    'status': 'danger',
                    'message': form.errors
                }
        return JsonResponse(response_data)
