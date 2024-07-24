from django.urls import path
from .import views
urlpatterns=[
    path('',views.home,name='homepage'),
    path('home/',views.home,name='homepage'),
    path('login/',views.login,name='loginpage'),
    path('register/',views.register,name='registerpage'),
    path('saveuser/',views.saveuser),
    path('verifyuser/',views.verifyuser),
    path('pred/',views.pred,name='prediction'),
    path('result/',views.result)
]