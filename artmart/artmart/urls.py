"""
URL configuration for artmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from myapp import views
from artmart import settings
from myapp.views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("register/", views.register, name='register'),
    path('artist_login/', views.artist_login, name='artist_login'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    # path('profile/', views.profile, name='profile'),

    path('artist/', views.artist, name='artist'),
    path('artist/<int:artist_id>/', views.view_artist_profile, name='view_artist_profile'),
   
    path('artwork/', views.artwork, name='artwork'),
    path('create_artwork/',views.create_artwork, name='create_artwork'),
    path('artwork/<int:artwork_id>/update/',views.edit_artwork, name='edit_artwork'),
    path('artist_artworks/', artist_artworks, name='artist_artworks'),
    path('artwork/<int:artwork_id>/', views.artwork_detail, name='artwork_detail'),
    path('artwork/delete/<int:artwork_id>/', views.artwork_delete, name='delete_artwork'),


    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:artwork_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_history/', views.order_history, name='order_history'),
    path('artwork/<int:artwork_id>/review/', views.leave_review, name='leave_review'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)