from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name= 'home'),
    path('home', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('scrap_products', views.scrap_products, name='scrap_products'),
    path('detail/<int:product_id>', views.detail, name='detail'),
    path('compare/', views.compare, name='compare'),
    path('filter_products/', views.filter_products, name='filter_products'),
    path('graphics/', views.graphics, name='graphics'),
    path('search/', views.search_results, name='search'),
    path('laptop/', views.laptop, name='laptop'),
    
    path('smartphone/', views.Smartphone, name='smartphone'),
]