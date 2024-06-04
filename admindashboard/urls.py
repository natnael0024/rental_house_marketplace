from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',  views.dashboard,  name='admin-dashboard' ),
    path('users',  views.get_users,  name='admin-users' ),
    path('users/<int:id>/action',  views.ban_unban_user,  name='admin-action'),
    path('ads',  views.create_add,  name='admin-ads'),
    path('ads/<int:id>',  views.set_ad_status,  name='admin-ads-status'),
]
