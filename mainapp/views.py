from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop - главная'
    }
    return render(request, 'mainapp/index.html', context)

def products(request, category_id=None, page=1):
    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('price')
    else:
        products = Product.objects.all()
    context = {
        'title': 'GeekShop - продукты',
        'categories': ProductCategory.objects.all(),
        'product_list': products
    }
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context.update({'product_list': products_paginator})

    return render(request, 'mainapp/products.html', context)