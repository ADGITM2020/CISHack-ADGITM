from django.contrib import admin
from .models import Product, Invoice, Company, InvoiceProduct, Vehicle

admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Company)
admin.site.register(InvoiceProduct)
admin.site.register(Vehicle)
