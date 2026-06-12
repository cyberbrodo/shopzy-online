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
            price = models.IntegerField()
            offer_price = models.IntegerField(null=True, blank=True)
            stock = models.IntegerField(default=1)
            is_offer = models.BooleanField(default=False)

            def __str__(self):
                return self.name

class Cart(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        quantity = models.IntegerField(default=1)

        def get_total_price(self):
          return self.quantity * self.product.price

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to="product_more_images")

    def __str__(self):
        return self.product.name