from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from bill.models import Product, InvoiceProduct


# def current_stock(request):
#     product = Product.objects.all()
#     return render(request, 'inventory/current_stock.html', {"products": product})

@login_required()
def add_stock(request):
    return render(request, 'inventory/product_study.html')


@method_decorator(login_required, name="dispatch")
class ProductDetail(DetailView):
    model = Product
    template_name = 'inventory/product_study.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        all_orders = InvoiceProduct.objects.filter(item=self.object).order_by("-bill_no__bill_date")
        if all_orders.count() > 20:
            required_orders = all_orders[:20]
        else:
            required_orders = all_orders
        resultant_orders = required_orders.only('bill_no__invoice_no', 'bill_no__bill_date',
                                                'bill_no_id', 'total', 'quantity')
        context['Orders'] = resultant_orders
        return context


class StockList(ListView):
    model = Product
    template_name = 'inventory/current_stock.html'
    queryset = Product.objects.all()
