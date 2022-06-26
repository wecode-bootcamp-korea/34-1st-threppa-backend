from django.urls import path

from products.views import *

urlpatterns = [
    path('/detail', ProductDetailView.as_view()),
    path('/cart', CartView.as_view())
]