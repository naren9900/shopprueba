from django.urls import path
from . import views
from .views import productsByCategory

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('productsByCategory/<int:category_id>', views.productsByCategory, name='productsByCategory'),
    path('productByName', views.searchProductName, name='productByName'),
    path('productDetail/<int:product_id>', views.productDetail, name='productDetail'),
    path('carrito', views.shoppingCart, name='shoppingCart'),
    path('agregarCarrito/<int:product_id>', views.addCart, name='addCart'),
    path('eliminarProductosCarrito/<int:product_id>', views.removeProductsCart, name='removeProductsCart'),
    path('limpiarCarrito', views.cleanCart, name='cleanCart'),
    path('crearUsuario', views.createUser, name='createUser'),
    path('cuenta', views.userAccount, name='cuenta'),
    path('actualizarCliente', views.updateCustomer, name='updateCustomer'),
    path('login/', views.loginUser, name='loginUser'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    path('registrarPedido', views.registerOrder, name='registerOrder'),
]