from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from .models import Subscriber
from .forms import NewsletterSubscriptionForm


def subscribe_newsletter(request):
    response_data = {'success': False, 'message': ''}

    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                # Create a new Subscriber instance
                subscriber = Subscriber(email=email)
                subscriber.full_clean()  # Validate the model fields (including uniqueness)
                subscriber.save()

                context = {'email': subscriber.email}
                email_content = render_to_string('sub_thank_you_email.html', context)

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

                response_data['success'] = True
                response_data['message'] = 'Successfully subscribed to the newsletter.'
            except ValidationError as e:
                error_message = e.message_dict.get('email', [''])[0]

                response_data['message'] = error_message
        else:
            response_data['message'] = 'Invalid email address.'
    else:
        response_data['message'] = 'Invalid request method.'

    return JsonResponse(response_data)


def un_subscribe_newsletter(request):
    response_data = {'success': False, 'message': ''}

    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                # Create a new Subscriber instance
                subscriber = Subscriber.objects.filter(email=email).first()
                if subscriber:
                    # The email exists, remove the subscriber
                    email = subscriber.email
                    subscriber.delete()

                    context = {'email': email}
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

                    response_data['success'] = True
                    response_data['message'] = 'Successfully un-subscribed from the newsletter.'
                
                else:
                    response_data['message'] = f'No email matching {email}'

            except ValidationError as e:
                error_message = e.message_dict.get('email', [''])[0]

                response_data['message'] = error_message
        else:
            response_data['message'] = 'Invalid email address.'
    else:
        response_data['message'] = 'Invalid request method.'

    return JsonResponse(response_data)


