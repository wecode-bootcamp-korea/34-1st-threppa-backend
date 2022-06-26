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