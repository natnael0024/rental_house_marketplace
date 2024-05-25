from django.urls import path
from .views import login_view, register, logout, home_view

urlpatterns = [
    path('login', login_view, name='login_view'),
    path('signup', register,name='register'),
    path('logout', logout,name='logout'),
    path('home', home_view,name='home'),

]