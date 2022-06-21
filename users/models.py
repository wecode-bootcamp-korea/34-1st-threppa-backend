from django.db import models

class User(models.Model):
    username         = models.CharField(max_length=45, unique=True)
    first_name       = models.CharField(max_length=45)
    last_name        = models.CharField(max_length=45)
    email            = models.EmailField(max_length=200, unique=True)
    password         = models.CharField(max_length=200)
    phone_number     = models.CharField(max_length=100, unique=True)
    create_at        = models.DateField(auto_now_add=True)
    carts            = models.ManyToManyField("products.Product_Option", related_name="Cart")
    wish_lists       = models.ManyToManyField("products.Product_Option", related_name="Wish_list")

    class Meta:
        db_table = 'users'


class Review(models.Model):
    users        = models.ForeignKey(User, on_delete=models.CASCADE)
    products     = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name="product_reviews")
    review_texts = models.TextField()
    create_at    = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'