from django.shortcuts import render

# Create your views here.


def wallet(request):
    vendor = request.user.vendor
    context = {'vendor': vendor}

    return render(request, 'wallet/wallet.html', context)