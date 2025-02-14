
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Стартовая страница
    path('items/', views.item_list, name='item_list'),
    path('add/', views.add_item, name='add_item'),
    path('detail/<int:item_id>/', views.item_detail, name='item_detail'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('expired/', views.expired_items, name='expired_items'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('export/', views.export_to_excel, name='export_to_excel'),
]