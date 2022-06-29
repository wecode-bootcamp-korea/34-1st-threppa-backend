import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from django.db        import IntegrityError

from products.models  import Product, ProductOption, Size, Cart, Color
from products.utils   import login_required

class ProductView(View):
    def get(self, request, product_id):
        try:
            """
            {'id': 1, 'name': 'RED', 'image_url': 'http://............'},
            {'id': 2, 'name': 'BLACK', 'image_url': 'http://............'},
            {'id': 3, 'name': 'BLUE', 'image_url': 'http://............'},
            {'id': 4, 'name': 'RED', 'image_url': 'http://............'},
            {'id': 5, 'name': 'RED', 'image_url': 'http://............'},
            {'id': 6, 'name': 'RED', 'image_url': 'http://............'}]

            {
                'RED': {
                    'color_id': 1,
                    'images': [
                        'http://............',
                        'http://............',
                        'http://............',
                        'http://............'
                    ]
                },
                'BLACK': {'color_id': 1, 'images': ['http://............']},
                'BLUE': {'color_id': 1, 'images': ['http://............']}}
            """
            product = Product.objects.get(id = product_id)
            colors  = {color["name"] : {'color_id' : color.color.id, 'images'   : []} for color in product.colors.all()}

            for color in colors:
                colors[color["name"]]['images'].append(color["url"])

            result = {
                'product_id' : product.id,
                'name'       : product.name,
                'price'      : product.price,
                'colors'     : colors
            }

            return JsonResponse({"result" : result}, status=200)

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

            product_option = ProductOption.objects.get(
                product_id = data['product_id'],
                color_id   = data['color_id'],
                size_id    = data['size_id']
            )

            cart, created = Cart.objects.get_or_create(
                user_id           = user.id,
                product_option_id = product_option.id,
                defaults          = {'quantity' : data['quantity']}
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

            # TODO : product image 테이블을 별도로 생성할 필요가 있습니다. (데이터 관리 + 코드 가독성 증가)
            'image_url'    : cart.product_option.color.products_colors_images.first().image_url
        } for cart in carts ]
            
        return JsonResponse({"result": carts}, status=200)
