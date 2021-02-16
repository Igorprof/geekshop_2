from django.shortcuts import render
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator

from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)

def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = ProductCategory.objects.get(pk=pk)
            cache.set(key, category)
        return category
    else:
        return ProductCategory.objects.get(pk=pk)

def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category_id=pk).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category_id=pk).order_by('price')

def index(request):
    context = {
        'title': 'GeekShop - главная'
    }
    return render(request, 'mainapp/index.html', context)

@cache_page(3600)
def products(request, category_id=None, page=1):
    if category_id:
        # products = Product.objects.filter(category_id=category_id).order_by('price')
        products = get_products_in_category_ordered_by_price(category_id)
    else:
        products = Product.objects.all()
    context = {
        'title': 'GeekShop - продукты',
        # 'categories': ProductCategory.objects.all(),
        'categories': get_links_menu(),
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