from django.urls import path

from products.views import ProductListView, CartView, SizeView, ProductView, CategoryView, NavView, UserNavView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('/sizes', SizeView.as_view()),
    path('/carts', CartView.as_view()),
    path('', ProductListView.as_view()),
    path('/categories', CategoryView.as_view()),
    path('/nav', NavView.as_view()),
    path('/user_nav', UserNavView.as_view())
]