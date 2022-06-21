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
    name       = models.CharField(max_length=45)
    price      = models.DecimalField(10, 2)
    gender     = models.ForeignKey(GenderType, on_delete=models.CASCADE, related_name="gender_type_products")
    is_adult   = models.BooleanField(default=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collection_products")
    category   = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_products")
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'products'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class Size(models.Model):
    size = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'

class ImageUrl(models.Model):
    url = models.CharField(max_length=200)

    class Meta:
        db_table = 'image_urls'

class ProductColorImage(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_product_color_images")
    color     = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color_product_color_images")
    image_url = models.ForeignKey(ImageUrl, on_delete=models.CASCADE, related_name="image_url_product_color_images")

    class Meta:
        db_table = 'product_color_images'

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_product_options")
    color   = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color_product_options")
    sizes   = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_product_options")
    stock   = models.IntegerField()

    class Meta:
        db_table = 'product_options'