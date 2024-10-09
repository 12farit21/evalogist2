from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('search/', views.search_products, name='product_search'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.category_products, name='product_list_by_category'),  # Updated this to use the new view
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('twitter/', views.TwitterView.as_view(), name='twitter'),
]
