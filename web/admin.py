from django.contrib import admin

# Register your models here.
from .models import Category, Product

admin.site.register(Category)
#admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','registration_date', 'category')
    list_editable = ('price',)