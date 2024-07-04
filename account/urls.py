from django.urls import path
from . import views

urlpatterns = [
    # User Auth URLs
    path('register/', views.register, name='register'),
    path('account/login/', views.login_page, name='login'),
    path(f'account/logout/', views.log_out, name='log_out'),
    # path('subscription/', views.sub_grouping, name='sub'),
    path('category/', views.sub_category, name='category'),
    # Profile URLs
    path('profile', views.user_profile, name='profile'),
    # Products-Orders and Actions URLSs
    path('merchant', views.user_prod_stats, name='prod_stats'),
    path('delete/<int:pk>/', views.remove_product, name='delete_prod'),
    path('delete/<int:pk>/order/', views.remove_order, name='delete_order')
]
