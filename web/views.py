from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Client, SaleOrder, SaleOrderLine
from . cart import Cart

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from .forms import ClientForm





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

"""======================================================
        VISTAS PARA EL CARRITO DE COMPRA
======================================================"""

def shoppingCart(request):
    return render(request,'carrito.html')

def addCart(request,product_id):
    #agregar productos al carrito
    if request.method == 'POST':
        amount = int(request.POST['cantidad'])
    else:
        amount = 1

    objProduct = Product.objects.get(pk=product_id)
    cartProduct = Cart(request)
    cartProduct.add(objProduct, amount)

    print(request.session.get("cart"))

    return render(request, 'carrito.html')

def removeProductsCart (request, product_id):
    objProduct = Product.objects.get(pk=product_id)
    cartProduct = Cart(request)
    cartProduct.delete(objProduct)
    return render(request, 'carrito.html')

def cleanCart(request):
    cartProduct = Cart(request)
    cartProduct.clear()

    return render(request, 'carrito.html')


@csrf_protect
def createUser(request):
    if request.method == 'POST':
        dataUser = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        if not dataUser or not dataPassword:
            return render(request, 'login.html', {
                'error': 'Usuario y contraseña son obligatorios.',
                'nuevoUsuario': dataUser
            })

        try:
            # En SQLite, mantener atómicas cortas ayuda a evitar bloqueos
            with transaction.atomic():
                newUser = User.objects.create_user(username=dataUser, password=dataPassword)


        except IntegrityError:
            return render(request, 'login.html', {
                'error': 'Ese nombre de usuario ya está en uso. Elige otro.',
                'nuevoUsuario': dataUser

            })

        except Exception as e:
            # Si vuelve a aparecer "database is locked", lo indicamos al usuario
            return render(request, 'login.html', {
                'error': f'No se pudo crear el usuario. Intenta nuevamente. Detalle: {str(e)}',
                'nuevoUsuario': dataUser
            })

        if newUser is not None:
            login(request,newUser)# Guardar los datos en el navegador
            return redirect('/cuenta')

    return render(request, 'login.html')

def userAccount(request):
    try:
        clienteEditar = Client.objects.get(user_id= request.user)
        dataClient = {
            'dni':clienteEditar.dni,
            'name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            'phone': clienteEditar.telefono,
            'sexo': clienteEditar.sexo,
            'address': 'kr 2 cll 151',
            'birthdate': clienteEditar.fecha_nacimiento,
        }
    except:
        dataClient = {
            'name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

    formClient = ClientForm(dataClient)#para llenar la data en el formulario
    context = {
        'formClient':formClient
    }
    return render(request, 'cuenta.html', context)


def updateCustomer(request):
    if request.method=='POST':
        formClient = ClientForm(request.POST)
        if formClient.is_valid():#valida todos los campos del formulario si esta bien
            dataClient = formClient.cleaned_data #prepara la data para que ya se puede guardar limpia caracteres

            # Actualizar usuario
            actUser = User.objects.get(pk=request.user.id)
            actUser.first_name = dataClient['name']
            actUser.last_name = dataClient['last_name']
            actUser.email = dataClient['email']
            actUser.save()

            # Registrar Cliente

            editClient = Client.objects.get(user_id=actUser.id)
            if not editClient:
                newClient = ()
                newClient.user_id = actUser
                newClient.dni = dataClient['dni']
                newClient.telefono = dataClient['phone']
                newClient.sexo = dataClient['sexo']
                newClient.fecha_nacimiento = dataClient['birthdate']
                #newClient.direccion = dataClient['address']
                newClient.save()
            else:
                editClient.dni = dataClient['dni']
                editClient.telefono = dataClient['phone']
                editClient.sexo = dataClient['sexo']
                editClient.fecha_nacimiento = dataClient['birthdate']
                editClient.direccion = dataClient['address']
                editClient.save()

            message="Datos Actualizados prueba"
            context = {
                'mensaje': message,
                'formClient': formClient,
            }
            return render(request, 'cuenta.html', context)

    return render(request, 'index.html')

def loginUser(request):
    paginaDestino = request.GET.get('next')
    context = {
        'destino':paginaDestino
    }
    if request.method == 'POST':
        dataUser = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']

        userAuth = authenticate(request, username=dataUser, password=dataPassword)
        if userAuth is not None:
            login(request,userAuth)
            if dataDestino != 'None':
                return redirect(dataDestino)
            return redirect('/cuenta')
        else:
            context ={
                'messageError': 'Datos Incorrectos'
            }
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return render(request, 'login.html')

@login_required(login_url='/login/')
def registerOrder(request):
    try:
        clienteEditar = Client.objects.get(user_id= request.user)
        dataClient = {
            'dni':clienteEditar.dni,
            'name':request.user.first_name,
            'last_name':request.user.last_name,
            'email':request.user.email,
            'phone': clienteEditar.telefono,
            'sexo': clienteEditar.sexo,
            'address': 'kr 2 cll 151',
            'birthdate': clienteEditar.fecha_nacimiento,
        }
    except:
        dataClient = {
            'name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }


    formClient = ClientForm(dataClient)
    context = {
        'formClient':formClient
    }

    return render(request, 'pedido.html', context)

