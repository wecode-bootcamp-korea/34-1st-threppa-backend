import json

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction, IntegrityError

from products.models import *
from products.utils  import login_decorator

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

            product_detail ={
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
                color_id   = data['color_id'],
                size_id    = data['size_id']
            ).id

            cart_object = Cart.objects.filter(user_id = user.id, product_option_id = product_option_id)

            if not cart_object.exists():
                Cart.objects.create(user_id = user.id, product_option_id = product_option_id)
                cart_object.update(quantity = data['quantity'])
                return JsonResponse({"message" : "CREATE_CART_SUCCESS"}, status=201)

            else:
                cart_object.update(quantity = data['quantity'])
                return JsonResponse({"message" : "UPDATE_CART_SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)

    @login_decorator
    def get(self, request):
        user  = request.user

        carts = Cart.objects.filter(user_id = user.id)

        cart_detial =[{
            'product_id'   : cart.product_option.product.id,
            'product_name' : cart.product_option.product.name,
            'color'        : cart.product_option.color.name,
            'size'         : cart.product_option.size.sizes,
            'quantity'     : cart.quantity,
            #  'image_url'    : cart.product_option.color.color_products_colors_images.image_url
        } for cart in carts ]
            
        return JsonResponse({"result": cart_detial}, status=200)