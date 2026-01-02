from django.urls import path
from . import views
from .views import productsByCategory

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('productsByCategory/<int:category_id>', views.productsByCategory, name='productsByCategory'),
    path('productByName', views.searchProductName, name='productByName'),
    path('productDetail/<int:product_id>', views.productDetail, name='productDetail'),
]
