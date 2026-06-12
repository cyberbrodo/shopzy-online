from django.shortcuts import render,redirect,get_object_or_404
from .models import *


def home(request):

    products = Product.objects.all()
    offer_products = Product.objects.filter(is_offer=True)
    banners = Banner.objects.filter(active=True)
    categories = Category.objects.all()

    context = {
        'products':products,
        'offer_products':offer_products,
        'banners':banners,
        'categories':categories,
    }

    return render(request,'index.html',context)

def category_products(request,slug):

    category = get_object_or_404(Category,slug=slug)

    products = Product.objects.filter(category=category)

    return render(request,'category.html',{
        'category':category,
        'products':products
    })

def product_details(request,slug):

    product = get_object_or_404(Product,slug=slug)

    return render(request,'product_details.html',{
        'product':product
    })

def add_to_cart(request,id):

    product = get_object_or_404(Product,id=id)

    cart_item,created = Cart.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def cart(request):

    cart_items = Cart.objects.all()

    total = 0

    for item in cart_items:
        total += item.get_total_price()

    return render(request,'cart.html',{
        'cart_items':cart_items,
        'total':total
    })

def remove_from_cart(request,id):

    item = get_object_or_404(Cart,id=id)

    item.delete()

    return redirect('cart')

def increase_quantity(request,id):
    item = get_object_or_404(Cart,id=id)
    item.quantity += 1
    item.save()
    return redirect('cart')


def decrease_quantity(request,id):
    item = get_object_or_404(Cart,id=id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


def checkout(request):
    cart_items = Cart.objects.all()

    total = 0
    for item in cart_items:
        total += item.get_total_price()

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


def place_order(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        payment_method = request.POST.get('payment_method')

        cart_items = Cart.objects.all()

        total = 0
        for item in cart_items:
            total += item.get_total_price()

        Order.objects.create(
            name=name,
            phone=phone,
            address=address,
            pincode=pincode,
            city=city,
            state=state,
            payment_method=payment_method,
            total=total
        )

        cart_items.delete()

        return redirect('home')


import razorpay
from django.conf import settings
from django.shortcuts import render

def checkout(request):

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID,
              settings.RAZORPAY_KEY_SECRET)
    )

    amount = 1099 * 100   # paisa

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request,'payment.html',{
        'payment': payment,
        'amount': amount
    })

from django.shortcuts import render

def payment(request):
    return render(request, 'payment.html')