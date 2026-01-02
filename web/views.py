from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Create your views here.

"""Vistas para el catalogo de productos"""
def index(request):
    list_product = Product.objects.all()
    list_category = Category.objects.all()
    for cat in list_category:
        print(f"La cantidad de produtos que pertenece a la categoria {cat.name}:")
        a =cat.product_set.all
        print(a)

    context = {'products':list_product,
               'categorys':list_category}
    return render(request, 'index.html', context)

def productsByCategory(request,category_id):
    """ Vista para filtrar productos por categoria"""
    category_id = Category.objects.get(pk=category_id)
    list_products = category_id.product_set.all
    list_categorys = Category.objects.all()
    context = {
        'categorys': list_categorys,
        'products':list_products
    }
    return render(request, 'index.html',context)

def searchProductName(request):
    """ vista para busqueda de producto por nombre usando el wibget de busqueda """
    name = request.POST['name']
    listProduct = Product.objects.filter(name__contains=name)
    listCategory = Category.objects.all()
    context = {
        'categorys':listCategory,
        'products':listProduct
    }
    return render(request, 'index.html',context)

def productDetail(request, product_id):
    """ Vista para el detalle de producto"""
    #objProduct = Product.objects.get(pk=product_id)
    objProduct = get_object_or_404(Product, pk=product_id)

    context = {
        'product':objProduct,
    }

    return render(request,'producto.html', context)