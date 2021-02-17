from datetime import date

from django import forms
from django.conf import settings

from .models import Invoice, InvoiceProduct


class InvoiceForm(forms.ModelForm):
    po_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS, initial=date.today)

    class Meta:
        model = Invoice
        exclude = ('sum_total', 'grand_total', 'round_fig',
                   'grand_total_final', 'invoice_igst', 'invoice_cgst', 'invoice_sgst', 'eway', 'year', 'invoice_url')


class ProductForm(forms.ModelForm):
    class Meta:
        model = InvoiceProduct
        exclude = ['bill_no', 'total']
