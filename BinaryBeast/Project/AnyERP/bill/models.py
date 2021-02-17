from datetime import date

from django.db import models


class Company(models.Model):
    company_name = models.CharField(max_length=80)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    gstin = models.CharField(primary_key=True, max_length=30)
    state_code = models.CharField(max_length=2)

    def __str__(self):
        return self.company_name


class Vehicle(models.Model):
    vehicle_driver = models.CharField(max_length=30)
    vehicle_no = models.CharField(max_length=20)

    def __str__(self):
        return self.vehicle_driver + "-" + self.vehicle_no


class Product(models.Model):
    product_id = models.CharField(max_length=20, primary_key=True)
    product_name = models.CharField(max_length=40)
    product_price = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    product_igst = models.DecimalField(max_digits=5, decimal_places=2)
    product_sgst = models.DecimalField(max_digits=5, decimal_places=2)
    product_cgst = models.DecimalField(max_digits=5, decimal_places=2)
    hsn_code = models.CharField(max_length=10)

    def __str__(self):
        return self.product_name + '-' + str(self.product_price)


class Invoice(models.Model):
    invoice_no = models.PositiveSmallIntegerField()
    bill_to = models.ForeignKey(Company, on_delete=models.CASCADE)
    payment_term = models.CharField(max_length=20, default="30.days")
    po_no = models.CharField(max_length=20)
    po_date = models.DateField(max_length=20)
    bill_date = models.DateField(default=date.today)
    cartage = models.DecimalField(max_digits=7, decimal_places=2)
    sum_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    invoice_igst = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    invoice_cgst = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    invoice_sgst = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grand_total_final = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    invoice_driver = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    eway = models.CharField(max_length=25, blank=True, null=True)
    ref_transport_name = models.CharField(blank=True, max_length=30)
    ref_transport_no = models.CharField(blank=True, max_length=30)
    invoice_url = models.URLField(null=True, blank=True, unique=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.invoice_no)


class InvoiceProduct(models.Model):
    bill_no = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='invoice')
    item = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='invoice_product')
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    packing = models.CharField(max_length=30)
    rate = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.item.product_name} {self.rate}"
