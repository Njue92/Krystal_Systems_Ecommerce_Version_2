from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, ProductForm
from .models import Vendor
from goods.models import Product
from django.utils.text import slugify


# Create your views here.
def index(request):
    newest_products = Product.objects.all()[0:8]

    return render(request, 'shop/landing_page.html', {'newest_products': newest_products})


def base(request):
    context = {}

    return render(request, 'shop/base.html', context)


def footer(request):
    context = {}

    return render(request, 'shop/footer.html', context)


def contact(request):
    context = {}

    return render(request, 'shop/contact-us.html', context)


def product(request):
    context = {}

    return render(request, 'shop/product.html', context)


def left_nav(request):
    context = {}

    return render(request, 'shop/left_bar.html', context)


def become_vend(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            context = {'form': form, 'vendor': vendor}  # Include the vendor object in the context

            return render(request, 'shop/vendor_adm.html', context)

    else:
        form = UserCreationForm()

    return render(request, 'shop/become_vend.html', {'form': form})


# def login_vie(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home_page')  # Redirect to the desired page after successful login
#         else:
#             error_message = 'Invalid credentials'  # Display an error message for failed login attempts
#     else:
#         error_message = 'Invalid Credentials'
#
#     return render(request, 'shop/login.html', {'error_message': error_message})


# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # Add your login logic here, e.g., authenticate user, check credentials
#             # and perform login action
#             return redirect('home_page')  # Replace 'home_page' with the appropriate URL name
#     else:
#         form = LoginForm()
#
#     return render(request, 'shop/login.html', {'form': form})

@login_required
def vendor_adm(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor == request.user.vendor:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False
    context = {'vendor': vendor, 'products': products, 'orders': orders}  # Include 'orders' in the context

    return render(request, 'shop/vendor_adm.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page')  # Redirect to the desired page after successful login
        else:
            error_message = 'Invalid credentials. Please try again!'  # Display an error message for failed login attempts
    else:
        error_message = None

    return render(request, 'shop/login1.html', {'error_message': error_message})


@login_required()
def add_post(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_adm')
    else:
        form = ProductForm()

    return render(request, 'shop/add_post.html', {'form': form})


@login_required
def order_tickets(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor == request.user.vendor:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False
    context = {'vendor': vendor, 'products': products, 'orders': orders}  # Include 'orders' in the context

    return render(request, 'shop/order_tickets.html', context)


def shop(request):
    # newest_products = Product.objects.all()[0:8]
    all_products = Product.objects.all()[0:8]

    return render(request, 'shop/shop.html', {'all_products':all_products})
