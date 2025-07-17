from django.conf import settings  # Correct import here
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('stocks/', stocks, name='stocks'),
    path('login/',loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('register/', register, name='register'),
    path('buy/<int:id>', buy, name='buy'),
    path('sell/<int:id>', sell, name='sell'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)