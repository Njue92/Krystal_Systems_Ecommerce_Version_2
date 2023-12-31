from django.shortcuts import render, redirect

from order.utilities import checkout, notify_vendor, notify_customer
from .cart import Cart
from django.shortcuts import render, get_object_or_404, redirect
from goods.models import Category, Product
import random
from .forms import CheckoutForm
from django.contrib import messages




# Create your views here.

def cart_detail(request):
    cart = Cart(request)

    form = CheckoutForm(request.POST)

    if form.is_valid():
        try:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            county = form.cleaned_data['county']
            location = form.cleaned_data['location']

            order = checkout(request, first_name, last_name, email, phone, county, location, cart.get_total_cost())

            cart.clear()

            notify_customer(order)
            notify_vendor(order)

            messages.success(request, 'Your order has been placed successfully')
        except Exception:
            messages.error(request, 'Your order has been placed successfully!!')

        return redirect('success')
    else:
        form = CheckoutForm

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart/cart.html')


def success(request):
    context = {}
    return render(request, 'cart/cart.html', context)
