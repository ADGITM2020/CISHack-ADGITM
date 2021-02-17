import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Routers Setting
from . import views
from .router import router

# Swagger Documentation Setting
schema_view = get_schema_view(
    openapi.Info(
        title="Saraswati Enterprises API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.saraswatienterprisesfbd.com/policies/terms/",
        contact=openapi.Contact(email="contact@saraswatienterprisesfbd.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('test/', views.send_mail_to, name='test'),
    path('contactus/', views.about_us, name='contact-us'),
    path('bill/', include('bill.urls')),
    path('inventory/', include('inventory.urls')),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('api/dashboard/', views.DashboardDataView.as_view(), name='api-dashboard'),
    path('api/product/<str:pk>/', views.ProductViewApi.as_view(), name='api-single-product'),
    path('api/product/stats/<str:pk>/', views.ProductStatisticApi.as_view(), name='api-single-product-stats'),
    path('api/products/', views.ProductsApi.as_view(), name='api-products'),
    path('api/v1/', include(router.urls)),
    path('api/v1/upload/', views.UploadView.as_view(), name='file-upload'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)