from django.urls import path
from . import views

urlpatterns = [
    path('new_store',views.new_store, name='new_store'),
    path('stores',views.stores, name='stores'),
    path('delete_store/<int:id>',views.delete_store, name='delete_store'),
    path('edit_store/<int:id>',views.edit_store, name='edit_store'),
    path('store/<int:id>',views.store, name='store'),
    path('new_pdv',views.new_pdv, name='new_pdv'),
    path('delete_pdv/<int:id_store>/<int:id_pdv>',views.delete_pdv, name='delete_pdv'),
    path('pdvs',views.pdvs, name='pdvs'),
]