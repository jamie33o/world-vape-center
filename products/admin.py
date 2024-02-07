# admin.py
from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .admin_utils.add_discount_actions import (apply_fifty_percentage_discount,
                                               apply_five_percentage_discount,
                                               apply_ten_percentage_discount,
                                               apply_twenty_percentage_discount,
                                               remove_discount)
from .models import Product, Category, Brand, MultiOption
from .forms import CustomActionForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'brand', 'price', 'discounted_price')
    list_filter = ('category', 'brand', 'options')
    list_editable = ('price',)  # Enable editing the price directly in the list view


    actions = [apply_fifty_percentage_discount,
               apply_twenty_percentage_discount,
               apply_ten_percentage_discount,
               apply_five_percentage_discount,
               'apply_multiple_choices',
               remove_discount,
               ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('apply_multiple_choices/',
                 self.admin_site.admin_view(
                     self.apply_multiple_choices_view),
                 name='apply_multiple_choices'),
        ]
        return custom_urls + urls

    def apply_multiple_choices(self, request, queryset):
        encoded_ids = ','.join(str(obj.id) for obj in queryset)
        url = reverse('admin:apply_multiple_choices') + f'?ids={encoded_ids}'
        return HttpResponseRedirect(url)

    def apply_multiple_choices_view(self, request):
        if request.method == 'POST':
            form = CustomActionForm(request.POST)
            if form.is_valid():
                ids = form.cleaned_data['ids']
                ids_list = [int(id) for id in ids.split(',')]
                queryset = Product.objects.filter(id__in=ids_list)
                selected_choices = form.cleaned_data['choices']
                options_name = form.cleaned_data['options_name']

                if selected_choices:
                    selected_options = MultiOption.objects.filter(id__in=selected_choices)

                    for product in queryset:
                        # Clear existing options and set the selected MultiOption instances
                        product.options.clear()
                        product.options_name = options_name
                        product.options.add(*selected_options)
                        product.save()

                    self.message_user(request, 'Choices applied to selected products.')
                    return HttpResponseRedirect('..')  # Redirect to the changelist page
        else:
            encoded_ids = request.GET.get('ids', '')
            queryset = Product.objects.filter(id__in=encoded_ids.split(','))
            form = CustomActionForm()

        return render(request, 'admin/admin_add_choices.html', {
            'form': form,
            'ids': encoded_ids,
            'products': queryset,
        })

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(MultiOption)
