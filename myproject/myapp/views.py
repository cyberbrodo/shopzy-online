from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import razorpay
from .models import Product, Category, Banner, Order, Cart, ProductImage, Review
from .models import Order, OrderItem
from myapp.models import Product




def home(request):
    products = Product.objects.all()
    offer_products = Product.objects.filter(is_offer=True)
    banners = Banner.objects.filter(active=True)
    categories = Category.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'offer_products': offer_products,
        'banners': banners,
        'categories': categories,
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    return render(request, 'category.html', {
        'category': category,
        'products': products
    })


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all().order_by('-id')

    if request.method == "POST":
        Review.objects.create(
            product=product,
            name=request.POST.get("name"),
            title=request.POST.get("title"),
            rating=request.POST.get("rating"),
            comment=request.POST.get("comment"),
            image=request.FILES.get("image")
        )
        return redirect('product_details', slug=product.slug)

    return render(request, 'product_details.html', {
        'product': product,
        'reviews': reviews
    })


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'image': product.image.url if product.image else '',
            'quantity': 1
        }

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, item in cart.items():
        item_total = item['price'] * item['quantity']
        total += item_total

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': item['price'],
            'image': item['image'],
            'quantity': item['quantity'],
            'total': item_total
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def increase_quantity(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def decrease_quantity(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        if cart[product_id]['quantity'] > 1:
            cart[product_id]['quantity'] -= 1
        else:
            del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    cart_items = []
    total = 0

    for product_id, item in cart.items():
        price = int(item['price'])
        quantity = int(item['quantity'])
        item_total = price * quantity
        total += item_total

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': price,
            'image': item['image'],
            'quantity': quantity,
            'total': item_total
        })

    amount = int(total * 100)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "amount": amount,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    })

def place_order(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})

        if not cart:
            return redirect('cart')

        total = 0
        for product_id, item in cart.items():
            total += item['price'] * item['quantity']

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            pincode=request.POST.get('pincode'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            payment_method="Prepaid",
            total=total
        )

        for product_id, item in cart.items():
            OrderItem.objects.create(
                order=order,
                product_name=item['name'],
                product_image=item['image'],
                price=item['price'],
                quantity=item['quantity'],
                total=item['price'] * item['quantity']
            )

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('my_orders')

    return redirect('cart')


def payment_success(request):
    return render(request, 'payment_success.html')

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart')




import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout


def send_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = str(random.randint(100000, 999999))

        request.session["login_email"] = email
        request.session["login_otp"] = otp

        print("SHOPZY LOGIN OTP:", otp)

        return redirect("verify_otp")

    return render(request, "send_otp.html")


def verify_otp(request):
    if request.method == "POST":
        entered_otp = (
            request.POST.get("otp1", "") +
            request.POST.get("otp2", "") +
            request.POST.get("otp3", "") +
            request.POST.get("otp4", "") +
            request.POST.get("otp5", "") +
            request.POST.get("otp6", "")
        )

        saved_otp = request.session.get("login_otp")
        email = request.session.get("login_email")

        if entered_otp == saved_otp and email:
            username = email.split("@")[0]

            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email}
            )

            login(request, user)

            request.session.pop("login_email", None)
            request.session.pop("login_otp", None)

            messages.success(request, "Login successful")
            return redirect("home")

        messages.error(request, "Invalid OTP")
        return redirect("verify_otp")

    return render(request, "verify_otp.html")


def profile(request):
    if not request.user.is_authenticated:
        return redirect("send_otp")

    return render(request, "profile.html")


def logout_user(request):
    logout(request)
    return redirect("home")

from django.contrib.auth.decorators import login_required

@login_required(login_url='send_otp')
def profile(request):
    return render(request, 'profile.html')

def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('send_otp')

    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'my_orders.html', {'orders': orders})
    