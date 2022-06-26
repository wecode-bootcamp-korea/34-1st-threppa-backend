from django.db import models

class User(models.Model):
    username         = models.CharField(max_length=45, unique=True)
    first_name       = models.CharField(max_length=45)
    last_name        = models.CharField(max_length=45)
    email            = models.EmailField(max_length=200, unique=True)
    password         = models.CharField(max_length=200)
    phone_number     = models.CharField(max_length=100, unique=True)
    created_at       = models.DateField(auto_now_add=True)
    # carts            = models.ManyToManyField("products.ProductOption", related_name="Cart")
    wish_lists       = models.ManyToManyField("products.ProductOption", related_name="Wish_list")

    class Meta:
        db_table = 'users'


class Review(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    product      = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="product_reviews")
    text         = models.TextField()
    created_at   = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'