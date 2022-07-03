from django.urls import path

from products.views import ProductListView, CartView, SizeView, ProductView, CategoryView, CartUpdateView, CategoryCollectionView, UserFullNameView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('/sizes', SizeView.as_view()),
    path('/carts', CartView.as_view()),
    path('/cartsupdate', CartUpdateView.as_view()),
    path('/list', ProductListView.as_view()),
    path('/categories', CategoryView.as_view()),
    path('/nav', CategoryCollectionView.as_view()),
    path('/user_nav', UserFullNameView.as_view())
]