from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login, name='login'),
    path('logout',views.user_logout, name='logout'),
    path('is-registered',views.is_registered, name='is_registered'),
    path('new-mac',views.new_mac, name='new_mac'),
    path('delete-mac/<int:id_mac>',views.delete_mac, name='delete_mac'),
    
    path('mac-control',views.mac_control, name='mac-control'),
]