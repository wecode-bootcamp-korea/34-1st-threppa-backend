from django.urls import path

from products.views import ProductListView, CartView, SizeView, ProductView, CategoryView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('/sizes', SizeView.as_view()),
    path('/carts', CartView.as_view()),
    path('/lists', ProductListView.as_view()),
    path('/categories', CategoryView.as_view())
]