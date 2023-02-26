from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('product_listing/', views.product_listing, name='product_listing'),
    path('product_listing_detail/<int:pk>', views.product_listing_detail, name='product_listing_detail'),
    path('testdrive_booking/<int:pk>',views.testdrive_booking, name='testdrive_booking'),
    path('addaccessories/<int:pk>', views.addaccessories, name='addaccessories'),
    path('taxinfo/<int:pk>', views.taxinfo, name='taxinfo'),
    path('booknow/<int:pk>', views.booknow, name='booknow'),
    path('add_to_cart/<int:oid>',views.add_to_cart,name='add_to_cart'),
    path('testdrive_booked/<int:oid>',views.testdrive_booked,name='testdrive_booked'),
    path('testdrivecart',views.testdrivecart,name='testdrivecart'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('shopping_cart_pdf/', views.shopping_cart_pdf, name='shopping_cart_pdf'),
    path('testdrive_pdf/', views.testdrive_pdf, name='testdrive_pdf'),
    path('testdrivecancel/<int:oid>',views.testdrivecancel,name='testdrivecancel'),
    path('tracking_order/', views.tracking_order, name='tracking_order'),
    path('cancelorder/<int:oid>',views.cancelorder,name='cancelorder'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('updaterecord', views.updaterecord, name='updaterecord'),
    path('favourite_products/', views.favourite_products, name='favourite_products'),
    path('checkout/', views.checkout, name='checkout'),
    path("payment/", views.order_payment, name="payment"),
    path("callback/", views.callback, name="callback"),
    path('error404/', views.error404, name='error404'),
    path('trail/', views.trail, name='trail'),
    path('trail2/', views.trail2, name='trail2'),
    path('trail3/', views.trail3, name='trail3'),
    path('trail4/', views.trail3, name='trail4'),
    path('trail5/',views.trail5, name='trail5'),
    path('trail6/',views.trail6, name='trail6'),
    path('rating/',views.rating, name='rating'),
    path('testdriverating/',views.testdriverating, name='testdriverating'),
    # path('search',views.search,name='search'),
    

    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name ='password_reset.html'),
    name="reset_password"),

    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name ='password_reset_sent.html'),
    name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name ='password_reset_form.html'),
    name='password_reset_confirm'),

    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name ='password_reset_done.html'),
    name='password_reset_complete')
]