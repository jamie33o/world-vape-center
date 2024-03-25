from datetime import timedelta
from profile.models import CustomUser
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils import timezone
from checkout.models import Order
from .models import Ticket
from .forms import (OrderStatusForm,
                    TicketStatusForm,
                    TicketForm,
                    TicketResponseForm)

@user_passes_test(lambda u: u.is_staff)
def orders_dashboard(request):
    """
    Render the orders dashboard.

    Returns:
        HttpResponse: Rendered orders dashboard.
    """
    template_name = 'dashboard/orders-dashboard.html'
    today = timezone.now()

    first_day_of_month = today.replace(day=1)
    last_day_of_month = (first_day_of_month.replace(month=(first_day_of_month.month % 12) + 1, day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59)
    start_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_year = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    annual_orders = Order.objects.filter(date__range=[start_of_year, end_of_year]).count()
    monthly_orders = Order.objects.filter(date__range=[first_day_of_month, last_day_of_month]).count()
    pending_orders = Order.objects.filter(status='pending').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    processing_orders = Order.objects.filter(status='processing').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()

    context = {
        'pending_orders': pending_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'processing_orders': processing_orders,
        'cancelled_orders': cancelled_orders,
        'total_orders': annual_orders,
        'monthly_orders': monthly_orders,
        'current_time': today
    }

    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
def orders(request, status):
    """
    Render the order list with the given status.

    Returns:
        HttpResponse: Rendered order list.
    """
    template_name = 'dashboard/order-list.html'

    orders = Order.objects.filter(status=status)
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')

    try:
        order_list = paginator.page(page)
    except PageNotAnInteger:
        order_list = paginator.page(1)
    except EmptyPage:
        order_list = paginator.page(paginator.num_pages)

    forms = [(order, OrderStatusForm(instance=order)) for order in order_list]

    context = {
        'status': status,
        'forms': forms,
        'order_list': order_list  
    }
    return render(request, template_name, context)


def change_order_status(request, order_id):
    """
    Change the status of an order.

    Returns:
        JsonResponse: JSON response indicating the status of the operation.
    """
    order = get_object_or_404(Order, pk=order_id)
    
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Status updated'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Could not update Status'}, status=500)


@user_passes_test(lambda u: u.is_staff)
def overview_dashboard(request):
    """
    Render the overview dashboard.

    Returns:
        HttpResponse: Rendered overview dashboard.
    """
    template_name = 'dashboard/overview-dashboard.html'
    today = timezone.now()
    current_year = today.year
    one_day = today - timedelta(days=1)
    first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_of_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month = first_day_of_month - timedelta(days=1)
    first_day_of_last_month = last_month.replace(day=1)
    last_day_of_month = (first_day_of_month.replace(month=(first_day_of_month.month % 12) + 1, day=1) - timedelta(days=1)).replace(hour=23, minute=59, second=59)
    current_month = timezone.now().month

    new_daily_users = CustomUser.objects.filter(date_joined__gte=one_day).count()
    monthly_user = CustomUser.objects.filter(date_joined__range=[first_day_of_month, last_day_of_month]).count()
    new_users_annually = CustomUser.objects.filter(date_joined__gte=first_day_of_year).count()
    last_month_users = CustomUser.objects.filter(date_joined__gte=first_day_of_last_month).count()
    annual_sales = Order.objects.filter(date__year=current_year).aggregate(total=Sum('grand_total'))['total']
    monthly_sales = Order.objects.filter(date__month=current_month).aggregate(total=Sum('grand_total'))['total']

    if annual_sales is None:
        annual_sales = 0
    if monthly_sales is None:
        monthly_sales = 0

    context = {
        'new_daily_users': new_daily_users,
        'monthly_user': monthly_user,
        'new_users_annually': new_users_annually,
        'last_month_users': last_month_users,
        'annual_sales': annual_sales,
        'monthly_sales': monthly_sales,
        'current_time': today,
    }

    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
def tickets_dashboard(request):
    """
    Render the tickets dashboard.

    Returns:
        HttpResponse: Rendered tickets dashboard.
    """
    template_name = 'dashboard/tickets-dashboard.html'

    total_open = Ticket.objects.filter(status=
                                        'Open').aggregate(count=
                                                               Count('id'))['count']
    total_closed = Ticket.objects.filter(status=
                                        'Closed').aggregate(count=
                                                               Count('id'))['count']

    questions = Ticket.objects.filter(title=
                                        'question').aggregate(count=
                                                               Count('id'))['count']
    site_error = Ticket.objects.filter(title=
                                        'site_error').aggregate(count=Count('id'))['count']
    order_issue = Ticket.objects.filter(title=
                                        'order_issue').aggregate(count=Count('id'))['count']
    delivery_issue = Ticket.objects.filter(title=
                                            'delivery_issue').aggregate(count=Count('id'))['count']
    refund_request = Ticket.objects.filter(title=
                                            'refund_request').aggregate(count=Count('id'))['count']
    account_issue = Ticket.objects.filter(title=
                                            'account_issue').aggregate(count=Count('id'))['count']
    feedback = Ticket.objects.filter(title=
                                        'feedback').aggregate(count=Count('id'))['count']
    other = Ticket.objects.filter(title=
                                    'other').aggregate(count=Count('id'))['count']

    context = {
        'questions': questions,
        'site_error': site_error,
        'order_issue': order_issue,
        'delivery_issue': delivery_issue,
        'refund_request': refund_request,
        'account_issue': account_issue,
        'feedback': feedback,
        'other': other,
        'total_open': total_open,
        'total_closed': total_closed
    }

    return render(request, template_name, context)


@user_passes_test(lambda u: u.is_staff)
def tickets(request, title):
    """
    Handle GET requests for the orders.

    Returns:
    - HttpResponse: Rendered profile page.
    """
    template_name = 'dashboard/ticket-list.html'

    # Retrieve all orders for the given status
    ticket_list = Ticket.objects.filter(title=title)

    # Paginate the orders
    paginator = Paginator(ticket_list, 10)
    page = request.GET.get('page')

    try:
        ticket_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ticket_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ticket_list = paginator.page(paginator.num_pages)

    forms = []

    for ticket in ticket_list:
        form = TicketStatusForm(instance=ticket)
        response_form = TicketResponseForm()
        forms.append((ticket, form, response_form))

    context = {
        'title': title,
        'forms':  forms,
        'ticket_list': ticket_list  
    }

    return render(request, template_name, context)


def change_ticket_status(request, ticket_id):
    """
    Change the status of a ticket.

    Returns:
        JsonResponse: JSON response indicating the status of the operation.
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = TicketStatusForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Status updated'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Could not update Status'}, status=500)


def open_ticket(request):
    """
    Open a new ticket.

    Returns:
        HttpResponse: Redirects to a specified URL.
    """
    ticket_form = TicketForm(request.POST)
    url = request.POST.get('url')
    if ticket_form.is_valid():
        ticket_form.instance.user = request.user
        ticket_form.save()
        messages.success(request, 'Ticket opened')
    else:
        messages.error(request, ticket_form.errors)
    return redirect(url)


def ticket_response(request, ticket_id):
    """
    Respond to a ticket.

    Returns:
        HttpResponse: Redirects to a specified URL.
    """
    ticket = Ticket.objects.get(id=ticket_id)
    ticket_response_form = TicketResponseForm(request.POST)
    url = request.POST.get('url')
    if ticket_response_form.is_valid():
        ticket_message = ticket_response_form.save(commit=False)
        ticket_message.sender = request.user
        ticket_message.ticket = ticket
        ticket_message.save()
        messages.success(request, 'Response sent')
    else:
        messages.error(request, ticket_response_form.errors)
    return redirect(url)
