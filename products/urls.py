from django.urls import path

from products.views import *

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/sizes', SizeView.as_view())
]