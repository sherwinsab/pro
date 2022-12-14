from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('product_listing/', views.product_listing, name='product_listing'),
    path('product_listing_detail/', views.product_listing_detail, name='product_listing_detail'),
]