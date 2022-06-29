import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from django.db        import transaction, IntegrityError

from products.models  import *
from products.utils   import login_decorator

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)

            product_color_images = product.product_products_colors_images.all()

            colors = [{
                'id'        : product_color_image.color.id,
                'name'      : product_color_image.color.name,
                'image_url' : product_color_image.image_url
            } for product_color_image in product_color_images ]

            product_detail = {
                'product_id' : product.id,
                'name'       : product.name,
                'price'      : product.price,
                'colors'     : colors
            }

            return JsonResponse({"results" : product_detail}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST"}, status=400)

class SizeView(View):
    def get(self, request):
        return JsonResponse({"sizes" : list(Size.objects.values("id", "sizes"))}, status=200)

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user

            product_option_id = ProductOption.objects.get(
                product_id = data['product_id'],
                color_id   = Color.objects.get(name = data['color']).id,
                size_id    = Size.objects.get(sizes = data['size']).id
            ).id

            object, created = Cart.objects.update_or_create(
                user_id = user.id, product_option_id = product_option_id, 
                defaults={'quantity': data['quantity']}
                )

            return JsonResponse({"message" : "UPDATE_CART_SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)

    @login_decorator
    def get(self, request):
        user  = request.user

        carts_dbs = Cart.objects.filter(user_id = user.id)

        carts =[{
            'product_id'   : carts_db.product_option.product.id,
            'product_name' : carts_db.product_option.product.name,
            'color'        : carts_db.product_option.color.name,
            'size'         : carts_db.product_option.size.sizes,
            'quantity'     : carts_db.quantity,
            'price'        : carts_db.product_option.product.price,
            'image_url'    : carts_db.product_option.color.color_products_colors_images.first().image_url
        } for carts_db in carts_dbs ]
            
        return JsonResponse({"result": carts}, status=200)

class ProductListView(View):
    def get(self, request):
        category = request.GET.get('category_id')
        collection = request.GET.get('collection_id')
        color = request.GET.get('color_name')
        # offset = int(request.GET.get('offset', 10))
        # limit = int(request.GET.get('limit', 5))
        
        q = Q()
        
        if category:
            q &= Q(category_id=category)
        if collection:
            q &= Q(collection_id=collection)
        
        products = Product.objects.filter(q)
        # products = Product.objects.filter(category_id = category | collection_id = collection)
        # colors =
        
        # colors = [{
        #     'id'   : product.product_products_colors_images.first().color.id,
        #     'name' : product.product_products_colors_images.first().color.name,
        # } for product in products ]

        # sizes = [{
        #     'id'    : product.product_product_options.first().size.id,
        #     'sizes' : product.product_product_options.first().size.sizes
        # } for product in products ]

        product = [{
            "product_id" : product.id,
            "product_name" : product.name,
            "price" : product.price,
            "image_url" : product.product_products_colors_images.first().image_url,
            # "colors" : product.product_products_colors_images.first().color.name,
            # "sizes" : product.product_product_options.first().size.sizes
        }for product in products]

        return JsonResponse({"result": product}, status=200)