from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_items, name='prod_list'),
    path('<int:Id>/<str:pk>/', views.product_detail, name='prod_detail'),
    path('upload/', views.upload_product, name='prod_upload'),
    path('update/<int:pk>/', views.update_product, name='prod_update'),
    path('cart/', views.cart, name='cart'),
    path("add_cart/", views.add_to_cart, name="add_cart"),
    path('delete/<int:pk>/', views.remove_item, name='delete_item'),
    path('checkout/<int:pk>/', views.checkout, name='checkout'),
    path('search/', views.search_res, name='search'),

]
