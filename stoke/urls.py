from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create Account/', views.create_account, name='signup'),
    path('add/', views.add_product, name='add_product'),
    path('remove/', views.remove_product, name='remove_product'),
    
    path('get_product_details/', views.get_product_details, name='get_product_details'),
    path('handle/', views.handle, name='handle'),

]