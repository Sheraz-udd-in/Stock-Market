from django.urls import path,include
from .views import fun,fun1,fun2,fun3,fun4

urlpatterns = [
    path('' , fun, name= 'index'),
    path('market',fun1, name= 'market'),
    path('register',fun2, name= 'register'),
    path('login',fun3,name= 'login'),
    path('logout',fun4,name='logout')
]