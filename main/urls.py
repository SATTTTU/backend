from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name="index"),
    path('blog_single/',blog_single,name="blogsingle"),
    path('blog/',blog,name="blog"),
    path('cart/',cart,name="cart_detail"),
    path('checkout/',checkout,name="checkout"),
    path('contact/',contact,name="contact"),
    path('product_details/<int:id>',product_details,name="product_details"),
    path('shop/',shop,name="shop"),



    # """
    # ==============================================================
    #                            auth start
    # =============================================================
    # """
    path('login/',log_in,name="login"),
    path("profile/",customer_profile,name="profile"),
    path('register/',register,name='register'),
    path('logout/',logout,name="logout"),


    
    # ==============================================================
    #                            cart start
    # =============================================================
    path('cart/add/<int:id>', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>',item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>',item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/',cart_detail,name='cart_detail'),


    
   
   


]


    






    

