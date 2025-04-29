from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    # path('users/', views.view_users, name='users'),
    path('orders/', views.view_orders, name='orders'),
    path('inventory/', views.manage_inventory, name='inventory'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/<str:category>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/<str:category>/', views.delete_product, name='delete_product'),
]
