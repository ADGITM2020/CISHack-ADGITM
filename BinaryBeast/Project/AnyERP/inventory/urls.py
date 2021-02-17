from django.urls import path

from . import views

# namespace
app_name = 'inventory'

urlpatterns = [
    # inventory
    # url(r'^$', views.current_stock, name='current'),
    path('', views.StockList.as_view(), name='current'),
    path('product/<str:pk>/', views.ProductDetail.as_view(), name='study'),
]
