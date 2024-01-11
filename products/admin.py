# admin.py
from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .admin_utils.add_discount_actions import (apply_fifty_percentage_discount,
                                               apply_five_percentage_discount,
                                               apply_ten_percentage_discount,
                                               apply_twenty_percentage_discount,
                                               remove_discount)
from .models import Product, Category, Brand, MultiOption
from .forms import CustomActionForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'discounted_price')

    actions = [apply_fifty_percentage_discount,
               apply_twenty_percentage_discount,
               apply_ten_percentage_discount,
               apply_five_percentage_discount,
               'apply_choices_to_selected',
               remove_discount
               ]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('apply_choices_to_selected/',
                 self.admin_site.admin_view(
                     self.apply_choices_to_selected_view),
                 name='apply_choices_to_selected'),

        ]
        return custom_urls + urls

    def apply_choices_to_selected(self, request, queryset):
        encoded_ids = ','.join(str(obj.id) for obj in queryset)
        url = reverse('admin:apply_choices_to_selected') + \
            f'?ids={encoded_ids}'
        return HttpResponseRedirect(url)

    def apply_choices_to_selected_view(self, request):

        if request.method == 'POST':
            form = CustomActionForm(request.POST)
            if form.is_valid():
                ids = form.cleaned_data['ids']

                ids_list = [int(id) for id in ids.split(',')]

                queryset = Product.objects.filter(id__in=ids_list)

                selected_choice = form.cleaned_data['choices']
                if selected_choice:
                    selected_option_id = selected_choice[0]
                    selected_option = get_object_or_404(MultiOption, id=selected_option_id)

                for product in queryset:
          
                    # Clear existing options and set the selected MultiOption instances
                    product.option = selected_option
                    product.save()

                self.message_user(
                    request, 'Choices applied to selected products.')
                # Redirect to the changelist page
                return HttpResponseRedirect('..')
        else:
            encoded_ids = request.GET.get('ids', '')
            queryset = Product.objects.filter(id__in=encoded_ids).values_list('name')

            form = CustomActionForm()

        return render(request, 'admin/admin_add_choices.html', 
                      {'form': form, 'ids': str(encoded_ids), 'product_name': queryset})


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(MultiOption)
