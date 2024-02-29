from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string

from .admin_utils.add_discount_actions import (apply_fifty_percentage_discount,
                                               apply_five_percentage_discount,
                                               apply_ten_percentage_discount,
                                               apply_twenty_percentage_discount,
                                               remove_discount)
from .models import Product, Category, Brand, MultiOption
from .admin_forms import (AdminAddMultiOptionForm,
                          AdminAddMultipleBrandsForm,
                          AdminAddPricesForm)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.

    List Display:
    - name
    - category
    - brand
    - price
    - discounted_price

    List Filter:
    - category
    - brand
    - options

    List Editable:
    - price

    Actions:
    - apply_fifty_percentage_discount
    - apply_twenty_percentage_discount
    - apply_ten_percentage_discount
    - apply_five_percentage_discount
    - remove_discount

    Custom URLs:
    - apply_multiple_choices/
    - apply_brand/
    - apply_prices/

    """

    list_display = ('name', 'category', 'brand',
                    'price',
                    'discounted_price')
    list_filter = ('category', 'brand', 'options')
    list_editable = ('price',)

    actions = [apply_fifty_percentage_discount,
               apply_twenty_percentage_discount,
               apply_ten_percentage_discount,
               apply_five_percentage_discount,
               remove_discount,
               ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('apply_multiple_choices/',
                 self.admin_site.admin_view(
                     self.apply_multiple_choices),
                 name='apply_multiple_choices'),
            path('apply_brand/',
                 self.admin_site.admin_view(
                     self.apply_brand),
                 name='apply_brand'),
            path('apply_prices/',
                 self.admin_site.admin_view(
                     self.apply_prices),
                 name='apply_prices'),
        ]
        return custom_urls + urls

    def apply_prices(self, request):
        """
        Admin action to apply prices to selected products.

        """
        if request.method == 'POST':
            form = AdminAddPricesForm(request.POST)

            if form.is_valid():
                ids = form.cleaned_data['ids']
                price = form.cleaned_data['price']

                ids_list = [int(id) for id in ids.split(',')]

                queryset = Product.objects.filter(id__in=ids_list)

                for product in queryset:
                    product.price = price
                    product.save()
                self.message_user(request, 'Price applied')
                return HttpResponseRedirect('..')
            self.message_user(request, 'Price not applied')
            return HttpResponseRedirect('..')

        form = AdminAddPricesForm()
        context = {'form': form, }
        html_content = render_to_string('admin/add-prices.html',
                                        context, request=request)
        response_data = {'html_content': html_content}
        return JsonResponse(response_data)

    def apply_brand(self, request):
        """
        Admin action to apply brands to selected products.

        """
        if request.method == 'POST':
            form = AdminAddMultipleBrandsForm(request.POST)

            if form.is_valid():
                ids = form.cleaned_data['ids']
                selected_brand_id = form.cleaned_data['brand']

                ids_list = [int(id) for id in ids.split(',')]

                queryset = Product.objects.filter(id__in=ids_list)
                selected_brand = get_object_or_404(Brand,
                                                   id=selected_brand_id)

                for product in queryset:
                    product.brand = selected_brand
                    product.save()
                self.message_user(request, 'Brands applied')
                return HttpResponseRedirect('..')
            self.message_user(request, 'Brands not applied')
            return HttpResponseRedirect('..')

        form = AdminAddMultipleBrandsForm()
        context = {'form': form, }
        html_content = render_to_string('admin/add-brands.html',
                                        context, request=request)
        response_data = {'html_content': html_content}
        return JsonResponse(response_data)

    def apply_multiple_choices(self, request):
        """
        Admin action to apply multiple choices to selected products.

        """
        if request.method == 'POST':
            form = AdminAddMultiOptionForm(request.POST)
            if form.is_valid():
                selected_choices = form.cleaned_data['choices']
                options_name = form.cleaned_data['options_name']

                ids = form.cleaned_data['ids']
                print(ids)
                ids_list = [int(id) for id in ids.split(',')]

                queryset = Product.objects.filter(id__in=ids_list)

                selected_options = MultiOption.\
                    objects.filter(id__in=selected_choices)

                for product in queryset:
                    # Clear existing options and set the
                    # selected MultiOption instances
                    product.options.clear()
                    product.options_name = options_name
                    product.options.add(*selected_options)
                    product.save()

                self.message_user(request,
                                  'Choices applied to selected products.')
                return HttpResponseRedirect('..')
            messages.error(request,
                           'Choices not applied to selected products.')

            return HttpResponseRedirect('..')
        else:
            form = AdminAddMultiOptionForm()
            context = {'form': form, }
            html_content = render_to_string('admin/admin_add_choices.html',
                                            context, request=request)
            response_data = {'html_content': html_content}
            return JsonResponse(response_data)


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(MultiOption)
