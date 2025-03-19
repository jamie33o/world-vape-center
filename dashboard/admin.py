from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now
from django.db.models import Sum
from django.contrib.auth import get_user_model
from checkout.models import Order
from datetime import timedelta
from django.utils import timezone
from .models import Ticket, TicketMessages


class TicketMessagesInline(admin.TabularInline):  
    """Inline admin for TicketMessages inside the Ticket panel."""
    model = TicketMessages
    extra = 1  
    readonly_fields = ('created_at',)
    ordering = ['-created_at']

class TicketAdmin(admin.ModelAdmin):
    """Admin customization for Ticket model."""
    
    list_display = ('id', 'title', 'status', 'user', 'message_count', 'new_messages', 'created_at')
    search_fields = ('title', 'status', 'user__email')
    list_filter = ('status', 'title', 'created_at')
    inlines = [TicketMessagesInline]

    def message_count(self, obj):
        """Show total messages in a ticket."""
        return obj.ticket_messages.count()
    message_count.short_description = "Total Messages"

    def new_messages(self, obj):
        """Highlight if new/unread messages exist."""
        unread_count = obj.ticket_messages.filter(is_read=False).count()
        if unread_count > 0:
            return format_html('<span style="color:red; font-weight:bold;">{} New</span>', unread_count)
        return "No New"
    
    new_messages.short_description = "New Messages"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        """
        Override Django Admin change view to mark messages as read when a ticket is opened.
        """
        ticket = self.get_object(request, object_id)
        if ticket:
            ticket.ticket_messages.filter(is_read=False).update(is_read=True)  # Mark messages as read
        return super().change_view(request, object_id, form_url, extra_context)

admin.site.register(Ticket, TicketAdmin)


### **✅ Step 1: Modify the Django Admin Homepage**
def custom_admin_index(request, *args, **kwargs):
    """Fetch statistics and render them inside the main Django Admin homepage."""
    current_time = now()
    User = get_user_model()

    # Get user statistics
    new_daily_users = User.objects.filter(date_joined__date=current_time.date()).count()
    monthly_user = User.objects.filter(date_joined__year=current_time.year, date_joined__month=current_time.month).count()
    last_month_users = User.objects.filter(date_joined__year=current_time.year, date_joined__month=current_time.month - 1).count()
    new_users_annually = User.objects.filter(date_joined__year=current_time.year).count()

    # Get sales data
    monthly_sales = Order.objects.filter(date__year=current_time.year, date__month=current_time.month).aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    annual_sales = Order.objects.filter(date__year=current_time.year).aggregate(Sum('grand_total'))['grand_total__sum'] or 0
    total_sales = Order.objects.all().aggregate(Sum('grand_total'))['grand_total__sum'] or 0

    today = timezone.now()

    first_day_of_month = today.replace(day=1)
    last_day_of_month = (
        first_day_of_month.replace(month=(first_day_of_month.month % 12) + 1, day=1)
        - timedelta(days=1)
    ).replace(hour=23, minute=59, second=59)
    start_of_year = today.replace(
        month=1, day=1, hour=0, minute=0, second=0, microsecond=0
    )
    end_of_year = today.replace(
        month=12, day=31, hour=23, minute=59, second=59, microsecond=999999
    )

    annual_orders = Order.objects.filter(
        date__range=[start_of_year, end_of_year]
    ).count()
    monthly_orders = Order.objects.filter(
        date__range=[first_day_of_month, last_day_of_month]
    ).count()
    pending_orders = Order.objects.filter(status="pending").count()
    shipped_orders = Order.objects.filter(status="shipped").count()
    processing_orders = Order.objects.filter(status="processing").count()
    delivered_orders = Order.objects.filter(status="delivered").count()
    cancelled_orders = Order.objects.filter(status="cancelled").count()
    total_orders = Order.objects.all().count()
    # Pass additional context
    kwargs["extra_context"] = {
        "new_daily_users": new_daily_users,
        "monthly_user": monthly_user,
        "last_month_users": last_month_users,
        "new_users_annually": new_users_annually,
        "monthly_sales": monthly_sales,
        "annual_sales": annual_sales,
        "total_sales": total_sales,

        "pending_orders": pending_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "processing_orders": processing_orders,
        "cancelled_orders": cancelled_orders,
        "annual_orders": annual_orders,
        "monthly_orders": monthly_orders,
        "total_orders": total_orders,
        "current_time": current_time,
    }

    return admin.site.__class__.index(admin.site, request, *args, **kwargs)


# **Override the Django Admin Homepage**
admin.site.index = custom_admin_index