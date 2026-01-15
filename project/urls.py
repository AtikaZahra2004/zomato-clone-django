"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('shop/',views.shop,name='shop'),
    
    path('blog/',views.blog,name='blog'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
  
    path('add_to_cart/<int:pk>',views.add_to_cart,name='add_to_cart'),
    
    path('cart/', views.cart_view, name='cart'),            # Cart page

    path('update/<int:pk>/<str:action>/' ,views.update,name='update'),
    
    path('remove/<int:pk>/', views.remove, name='remove'),

    path('check/',views.checkout,name='checkout'),
 

    path("success/<int:order_id>/", views.order_success, name="order_success"),
    
    path('profile/',views.profile,name='profile'),
    path('blog/blog1/',views.blog1,name='blog1'),
    path('blog/blog2/',views.blog2,name='blog2'),
    path('blog/blog3/',views.blog3,name='blog3'),
    path('blog/blog4/',views.blog4,name='blog4'),
    path('blog/blog5/',views.blog5,name='blog5'),
    path('blog/blog6/',views.blog6,name='blog6'),
    path('page/' ,views.page,name='page'),
    path('gallery/', views.gallery,name='gallery'),
    path('faq/' ,views.faq,name='faq'),
    path('test/', views.test,name='test'),
    path("orders/", views.order_history, name="order_history"),
    path("payment/",views.payment,name='payment'),
    path('payment-status',views.payment_status, name='payment-status') ,
    
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),






    



   
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

