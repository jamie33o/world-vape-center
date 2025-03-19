from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from .models import Order, OrderLineItem
from profile.models import ShippingAddress

class OrderLineItemInline(admin.TabularInline):
    """Inline admin to show line items inside an order."""
    model = OrderLineItem
    extra = 1  # Show an empty row to add a new line item
    readonly_fields = ('lineitem_total',)  # Prevent accidental edits
    ordering = ['-id']  # Show latest items first

class OrderAdmin(admin.ModelAdmin):
    """Customize admin panel for Orders."""
    
    list_display = ('order_number', 'user', 'email', 'status', 'status_action', 'formatted_line_items', 'formatted_shipping_address', 'sub_total', 'grand_total', 'date')
    list_editable = ('status',)  # Allow quick status updates
    search_fields = ('order_number', 'email', 'full_name')
    list_filter = ('status', 'date')
    readonly_fields = ('order_number', 'date', 'grand_total', 'sub_total', 'discount', 'formatted_line_items', 'formatted_shipping_address')
    inlines = [OrderLineItemInline]  # Attach line items to Order admin

    def status_label(self, obj):
        """Show colored status labels."""
        color_dict = {
            'pending': 'orange',
            'processing': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red'
        }
        color = color_dict.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_status_display())

    status_label.short_description = "Status"

    def status_action(self, obj):
        """Show a button to change the order status."""
        if obj.status == 'pending':
            return format_html('<a class="button" style="display:flex; background: #17a2b8; color: white; padding: 4px; text-decoration: none;  border-radius: 4px;" href="{}">Mark as Processing</a>',
                               reverse('admin:mark_order_processing', args=[obj.pk]))
        elif obj.status == 'processing':
            return format_html('<a class="button" style="display:flex; background: #6610f2; color: white; padding: 4px; text-decoration: none; border-radius: 4px;" href="{}">Mark as Shipped</a>',
                               reverse('admin:mark_order_shipped', args=[obj.pk]))
        elif obj.status == 'shipped':
            return format_html('<a class="button" style="display:flex; background: #28a745; color: white; padding: 4px; text-decoration: none; border-radius: 4px;" href="{}">Mark as Delivered</a>',
                               reverse('admin:mark_order_delivered', args=[obj.pk]))
        return "Completed"
    
    status_action.short_description = "Update Status"

    def formatted_line_items(self, obj):
        """Format order line items as 'Product (Quantity)' for readability."""
        line_items = obj.lineitems.all()
        if line_items:
            return format_html("<br>".join([f"{item.product.name} ({item.quantity})" for item in line_items]))
        return "No Items"
    
    formatted_line_items.short_description = "Order Items"

    def formatted_shipping_address(self, obj):
        """Format the shipping address for better readability."""
        address = obj.shipping_address
        if address:
            return format_html(
                "<strong>{}</strong><br>{}<br>{}<br>{}, {}<br>{}<br><strong>Phone:</strong> {}",
                address.user.get_full_name() if address.user else "No Name",
                address.street_address1,
                address.street_address2 if address.street_address2 else "",
                address.town_or_city,
                address.county if address.county else "",
                address.eircode if address.eircode else "No Eircode",
                address.phone_number
            )
        return "No Address"
    
    formatted_shipping_address.short_description = "Shipping Address"

    def get_urls(self):
        """Add custom admin URLs for the status update buttons."""
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path('mark_order_processing/<int:order_id>/', self.admin_site.admin_view(self.mark_order_processing), name='mark_order_processing'),
            path('mark_order_shipped/<int:order_id>/', self.admin_site.admin_view(self.mark_order_shipped), name='mark_order_shipped'),
            path('mark_order_delivered/<int:order_id>/', self.admin_site.admin_view(self.mark_order_delivered), name='mark_order_delivered'),
        ]
        return custom_urls + urls

    def mark_order_processing(self, request, order_id):
        """Mark the order as Processing."""
        order = Order.objects.get(pk=order_id)
        order.status = 'processing'
        order.save(update_fields=['status'])
        return redirect(request.META.get('HTTP_REFERER', 'admin:order_order_changelist'))

    def mark_order_shipped(self, request, order_id):
        """Mark the order as Shipped."""
        order = Order.objects.get(pk=order_id)
        order.status = 'shipped'
        order.save(update_fields=['status'])
        return redirect(request.META.get('HTTP_REFERER', 'admin:order_order_changelist'))

    def mark_order_delivered(self, request, order_id):
        """Mark the order as Delivered."""
        order = Order.objects.get(pk=order_id)
        order.status = 'delivered'
        order.save(update_fields=['status'])
        return redirect(request.META.get('HTTP_REFERER', 'admin:order_order_changelist'))

admin.site.register(Order, OrderAdmin)
