from django.contrib import admin
from .models import Category, Banner, Product, Cart, ProductImage,Review,ProductVariant


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'category', 'price', 'stock', 'is_offer']
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(ProductVariant)