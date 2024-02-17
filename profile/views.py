from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib import messages
from checkout.models import Order
from .models import Favourite, ShippingAddress
from .forms import ShippingAddressForm, ProfileUpdateForm



@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'profile/base.html'

    def get(self, request):
        user_address_instance = request.user.user_address.first()  # Assuming there's only one shipping address per user

        user_form = ProfileUpdateForm(instance=request.user)
        shipping_address_form = ShippingAddressForm(instance=user_address_instance)
        user_orders = Order.objects.filter(user=request.user)
        favourites = Favourite.objects.filter(user=request.user)

        context = {
            'user_form': user_form,
            'shipping_address_form': shipping_address_form,
            'user_orders': user_orders,
            'favourites': favourites
        }

        return render(request, self.template_name, context)


    def post(self, request):
        user_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile Updated!!')
        else:
            messages.error(request, user_form.errors)
            
        return redirect('profile')


@require_POST
def shipping_address_view(request):
    if not request.user.is_authenticated:
        messages.error(request, 'User not authenticated.')
        return redirect('login')  # Redirect to login or handle authentication as needed

    user_address_instance = request.user.user_address.first()

    if user_address_instance is None:
        # If the user doesn't have a shipping address, create a new instance
        user_address_instance = ShippingAddress(user=request.user)

    shipping_address_form = ShippingAddressForm(request.POST, instance=user_address_instance)

    if shipping_address_form.is_valid():
        shipping_address_form.save()
        messages.success(request, 'Shipping Address Updated!!')
    else:
        messages.error(request, 'Error updating shipping address. Please check the form.')

    return redirect('profile')
