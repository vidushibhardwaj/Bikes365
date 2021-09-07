from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
path('',views.home,name="home"),
path('signup/',views.user_signup,name="signup"),
path('login/',views.user_login,name="login"),
path('profile/',views.profile,name="profile"),
path('cart/',views.cart,name="cart"),
path('bikes/',views.bikes,name="bikes"),
path('about/',views.about,name="about"),
path('logout/',views.user_logout,name="user_logout"),
path('addTocart/<int:id>',views.addTocart,name="bikeadding"),
path('cancel/<int:id>',views.cancel_order,name="cancel_order"),
path('orderdetail/<int:id>',views.order_detail,name="orderdetail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
