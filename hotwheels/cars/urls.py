from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('product_listing/', views.product_listing, name='product_listing'),
    path('product_listing_detail/<int:pk>', views.product_listing_detail, name='product_listing_detail'),
    path('addaccessories/<int:pk>', views.addaccessories, name='addaccessories'),
    path('taxinfo/<int:pk>', views.taxinfo, name='taxinfo'),
    path('booknow/<int:pk>', views.booknow, name='booknow'),
    path('add_to_cart/<int:oid>',views.add_to_cart,name='add_to_cart'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('tracking_order/', views.tracking_order, name='tracking_order'),
    path('cancelorder/<int:oid>',views.cancelorder,name='cancelorder'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('favourite_products/', views.favourite_products, name='favourite_products'),
    path('error404/', views.error404, name='error404'),
    path('trail/', views.trail, name='trail'),
    path('trail2/', views.trail2, name='trail2'),
    path('trail3/', views.trail3, name='trail3'),
    path('trail4/', views.trail3, name='trail4'),
    path('trail5/',views.trail5, name='trail5'),
    path('trail6/',views.trail6, name='trail6'),
]