"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('product/<slug:slug>/', views.product_details, name='product_details'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),

    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    # path('payment-success/', views.payment_success, name='payment_success'),
path("login/", views.send_otp, name="send_otp"),
path("verify-otp/", views.verify_otp, name="verify_otp"),
path("ho/", views.verify_otp, name="index"),
path("profile/", views.profile, name="profile"),
path("logout/", views.logout_user, name="logout"),
path('my-orders/', views.my_orders, name='my_orders'),
]
