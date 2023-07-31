from django.shortcuts import render, get_object_or_404, redirect
import random
from django.db.models import Q
from .models import Category, Product
from .forms import AddToCartForm
from django.contrib import messages
from cart.cart import Cart


# Create your views here
def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return render(request, 'goods/search.html', {'products': products, 'query': query})


def product(request, category_slug, product_slug):
    # product = get_object_or_404(Product, product_id= category_slug, slug= product_slug)
    cart = Cart(request)
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            cart.add(product_id=product.id, quantity=quantity, update_quantity=False)

            messages.success(request, 'This item has been added to your Cart ')

            return redirect('product', category_slug=category_slug, product_slug=product_slug)

    else:
        form = AddToCartForm()

    similar_products = list(product.category.products.exclude(pk=product.pk))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    context = {
        'product': product,
        'similar_products': similar_products,
        'form': form
    }

    # return render(request, 'product.html', context)

    return render(request, 'goods/product_view.html', context)
