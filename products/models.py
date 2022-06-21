from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Collection(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'collections'

class Gender(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'genders'

class Product(models.Model):
    product_name = models.CharField(max_length=45)
    price        = models.IntegerField()
    genders      = models.ForeignKey(Gender, on_delete=models.CASCADE, related_name="gender_products")
    is_adult     = models.BooleanField(default=True)
    collections  = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collection_products")
    categories   = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_products")

    class Meta:
        db_table = 'products'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class Product_Color(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_products_colors")
    colors   = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color_products_colors")


    class Meta:
        db_table = 'products_colors'

class Product_Color_Image_Url(models.Model):
    products_colors = models.ForeignKey(Product_Color, on_delete=models.CASCADE, related_name="product_color_products_colors_image_urls")
    url             = models.CharField(max_length=200)

    class Meta:
        db_table = 'products_colors_image_urls'

class Size(models.Model):
    size = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'

class Product_Option(models.Model):
    products_colors_images = models.ForeignKey(Product_Color_Image_Url, on_delete=models.CASCADE, related_name="product_color_image_url_product_options")
    sizes                  = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size_product_options")
    stock                  = models.IntegerField()

    class Meta:
        db_table = 'product_options'