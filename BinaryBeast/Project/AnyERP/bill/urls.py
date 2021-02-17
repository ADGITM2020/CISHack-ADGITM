from django.urls import path

from . import views

# namespace
app_name = 'bill'

urlpatterns = [
    path('', views.BillSection.as_view(), name="bill-section"),
    # bill/logout
    path('logout/', views.logout_view, name='logout'),
    # bill/invoice
    path('create/', views.invoice_view, name='create'),
    # bill/chart
    path('chart/', views.chart_view, name='chart'),
    # bill/invoice/bill/download/pk
    path('download/<int:pk>/', views.download_excel, name='download'),
    path('<int:pk>/downloadpdf/', views.download_pdf, name='download-pdf'),
    path('<int:pk>/convertpdf/', views.convert_pdf, name='convert-pdf'),
    path('<int:pk>/generate/', views.generate_files, name='generate-files'),
    # /bill/pk/
    path('<int:pk>/', views.bill, name='info'),
    # bill/detail/
    path('detail/', views.invoice_detail, name='detail'),
    # bill/vehicle
    path('vehicle/', views.vehicle_register, name='vehicle'),
    # bill/vehicle/create
    path('vehicle/create/', views.create_vehicle, name='vehicle-create'),
]
