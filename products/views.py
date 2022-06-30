import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from products.models  import Product, ProductOption, Color, Size, Cart
from products.utils   import login_decorator

class ProductView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id = product_id)

            product_color_images = product.product_products_colors_images.all()

            colors = [{
                'id'        : product_color_image.color.id,
                'name'      : product_color_image.color.name,
                'image_url' : product_color_image.image_url
            } for product_color_image in product_color_images ]

            products = {
                'product_id' : product.id,
                'name'       : product.name,
                'price'      : product.price,
                'colors'     : colors
            }

            return JsonResponse({"results" : products}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST"}, status=400)

class SizeView(View):
    def get(self, request):
        return JsonResponse({"sizes" : list(Size.objects.values("id", "sizes"))}, status=200)

class ProductListView(View):
    def get(self, request):
        category   = request.GET.get('category_id')
        collection = request.GET.get('collection_id')
        offset     = int(request.GET.get('offset', 0))
        limit      = int(request.GET.get('limit', 5))
        
        q = Q()
        
        if category:
            q &= Q(category_id=category)
        if collection:
            q &= Q(collection_id=collection)
        
        products = Product.objects.filter(q)[offset:offset+limit]

        products = [{
            "product_id"   : product.id,
            "product_name" : product.name,
            "price"        : product.price,
            "colors"       :[{
                                "id"        : color.color.id,
                                "name"      : color.color.name,
                                "image_url" : color.image_url
                            } for color in product.product_products_colors_images.all()]
        } for product in products ]

        return JsonResponse({"result": products}, status=200)

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
            )

            cart, created = Cart.objects.get_or_create(
                user_id = user.id, 
                product_option_id = product_option_id.id, 
                defaults={'quantity': data['quantity']}
                )

            if not created:
                cart.quantity += data['quantity']
                cart.save()

            return JsonResponse({"message" : "UPDATE_CART_SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status = 400)

    @login_decorator
    def get(self, request):
        user  = request.user
        carts = Cart.objects.filter(user_id = user.id)

        carts =[{
            'product_id'   : cart.product_option.product.id,
            'product_name' : cart.product_option.product.name,
            'color'        : cart.product_option.color.name,
            'size'         : cart.product_option.size.sizes,
            'quantity'     : cart.quantity,
            'price'        : cart.product_option.product.price,
            'image_url'    : cart.product_option.color.color_products_colors_images.first().image_url
        } for cart in carts ]
            
        return JsonResponse({"result": carts}, status=200)