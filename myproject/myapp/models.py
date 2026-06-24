from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Banner(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='banner')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    price = models.IntegerField(null=True, blank=True)
    offer_price = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(default=1)
    is_offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_more_images")

    def __str__(self):
        return self.product.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    rating = models.IntegerField(default=5)
    image = models.ImageField(upload_to="reviews", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price


from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=50, default="Prepaid")
    total = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=50, default="Paid")
    order_status = models.CharField(max_length=50, default="Order Confirmed")
    tracking_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=200)
    product_image = models.CharField(max_length=500, blank=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    rating = models.IntegerField(default=5)
    image = models.ImageField(upload_to="reviews", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ProductVariant(models.Model):
            product = models.ForeignKey(
                Product,
                on_delete=models.CASCADE,
                related_name="variants"
            )
            color = models.CharField(max_length=50)
            stock = models.IntegerField(default=0)

            def __str__(self):
                return f"{self.product.name} - {self.color}"