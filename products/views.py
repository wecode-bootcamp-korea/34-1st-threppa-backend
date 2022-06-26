import json

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction, IntegrityError

from products.models import *
from products.utils  import login_decorator

class ProductDetailView(View):
    def get(self, request):
        try:
            data     = json.loads(request.body)
            product  = Product.objects.get(id = data['product_id'])
            sizes_db = Size.objects.all()
            
            sizes =[{ 
                'id'   : size_db.id,
                'size' : size_db.size
            } for size_db in sizes_db ]

            product_color_images = ProductColorImage.objects.filter(product_id = data['product_id'])

            colors = [{
                'id'        : product_color.color.id,
                'name'      : product_color.color.name,
                'image_url' : product_color.image_url
            } for product_color in product_color_images ]

            product_detail ={
                'product_id' : product.id,
                'name'       : product.name,
                'price'      : product.price,
                'colors'     : colors,
                'sizes'      : sizes
            }

            return JsonResponse({"results": product_detail}, status=201)

        except Product.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)

class CartView(View):
    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            data    = json.loads(request.body)

            user    = request.user

            product = Product.objects.get(id = data['product_id'])
            color   = Color.objects.get(id = data['color_id'])
            size    = Size.objects.get(id = data['size_id'])

            with transaction.atomic():
                product_option_created = ProductOption.objects.create(
                    product_id = product.id,
                    color_id   = color.id,
                    size_id    = size.id
                )

                Cart.objects.create(
                    user_id           = user.id,
                    product_option_id = product_option_created.id
                )

            return JsonResponse({"message": "CART_CREATE_SUCCESS"}, status=201)

        except IntegrityError:
            return JsonResponse({"message": "TRANSACTION_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)
    
    @login_decorator
    def get(self, request):
        try:
            user  = request.user

            carts = Cart.objects.filter(user_id = user.id)

            cart_detial =[{
                'product_id' : cart.product_option.product_id,
                'color_id'   : cart.product_option.color_id,
                'size_id'    : cart.product_option.size_id
            } for cart in carts ]
            
            return JsonResponse({"result": cart_detial}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST"}, status=400)