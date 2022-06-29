from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Collection(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'collections'

class GenderType(models.Model):
    type = models.CharField(max_length=45)

    class Meta:
        db_table = 'gender_types'

class Product(models.Model):
    name        = models.CharField(max_length=45)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    gender_type = models.ForeignKey(GenderType, on_delete=models.CASCADE, related_name="gender_type_products")
    is_adult    = models.BooleanField(default=True)
    collection  = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collection_products")
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_products")
    created_at  = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'products'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class Size(models.Model):
    sizes = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'

class ProductColor(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")
    color     = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="colors")
    url = models.URLField()
    
    class Meta:
        db_table = 'products_colors_images'

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_product_options")
    color   = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color_product_options")
    size    = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_product_options")
    stock   = models.IntegerField(null=True)

    class Meta:
        db_table = 'product_options'

class Cart(models.Model):
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_carts")
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="product_option_carts")
    quantity       = models.IntegerField(default=0)

    class Meta:
        db_table = 'carts'
