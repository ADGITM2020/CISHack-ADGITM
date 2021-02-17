import logging
import pdb

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Sum
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView
from django_filters import FilterSet
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from bill.models import Invoice, InvoiceProduct, Product
from inventory.serializers import ProductInvoiceSerializers, ProductSerializers, InvoiceProductSerializers
from saraswati_enterprises.login import LoginForm
from saraswati_enterprises.settings import StandardResultsSetPagination, EMAIL_HOST_USER

logger = logging.getLogger('django')


def home(request):
    return render(request, "home.html")


@method_decorator(login_required, name="dispatch")
class DashboardView(View, LoginRequiredMixin):
    template_name = 'bill/bill-section.html'

    def get_bill_queryset(self):
        invoices = Invoice.objects.order_by("-bill_date")
        return invoices

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html')

    def post(self, request, *args, **kwargs):
        bill_no = request.POST.get("bill_no", "")
        year = request.POST.get("year", "")
        if bill_no and year:
            invoices = Invoice.objects.filter(invoice_no=bill_no, year=year)
            if invoices.exists() and invoices.count() == 1:
                return redirect('bill:info', pk=invoices[0].pk)
            elif invoices.exists():
                return render(request, self.template_name, {'bills': invoices})
            raise Http404

        elif bill_no:
            invoices = Invoice.objects.filter(invoice_no=bill_no)
            if invoices:
                return render(request, self.template_name, {'bills': invoices})

        elif year:
            invoices = Invoice.objects.filter(year=year)
            if invoices:
                return render(request, self.template_name, {'bills': invoices})
        return redirect('bill:bill-section')


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def get(self, request, **kwargs):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        logger.warning("<<<<<<<<<<<<<<<<<---- wrong attemp")
        return render(request, self.template_name, {"form": form})


class DashboardDataView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        invoices = Invoice.objects.only('grand_total_final', 'bill_date', 'invoice_no', 'year')
        items_sold = invoices.count()
        total_sales = invoices.aggregate(sum=Sum('grand_total_final'))["sum"]
        orders = invoices.order_by("-bill_date")
        if orders.count() > 10:
            orders = orders[:10]
        price_invoice_data = orders.values_list('invoice_no', 'grand_total_final')
        invoice_list, price_list = zip(*price_invoice_data)
        unique_years = invoices.values_list('year', flat=True).distinct()
        if len(unique_years) > 5:
            unique_years = unique_years[:5]
        year_sales = map(
            lambda year: invoices.filter(year=year).aggregate(year_sum=Sum('grand_total_final'))['year_sum'],
            unique_years)
        data = {
            "price_list": list(price_list),
            "invoice_list": list(map(lambda x: f"INV{x}", invoice_list)),
            "year": unique_years,
            "yearSales": year_sales,
            "items_sold": items_sold,
            "total_sales": total_sales,
            "transaction": invoices.count()}
        return Response(data)


class ProductViewApi(APIView):
    authentication_classes = []
    permission_classes = []

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist as e:
            return Response({e: "given product not found."}, status=404)

    def get(self, request, pk=None):
        # product_data = {}
        product = self.get_object(pk)
        serializer = ProductInvoiceSerializers(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None):
        instance = self.get_object(pk)
        data = request.data
        serializer = ProductInvoiceSerializers(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ProductsApi(GenericAPIView, mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    permission_classes = []
    authentication_classes = []
    serializer_class = ProductSerializers
    # we are using custom filter class instead of the default pagination in the setting
    pagination_class = StandardResultsSetPagination
    # useful for caching feature
    queryset = Product.objects.all()

    # default lookup field is pk
    # we can set it by lookup_field = 'id'

    def get(self, request):
        return self.list(request)

    # def perform_create(self, serializer):
    #     serializer.save()

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk=None):
        return self.delete(request, pk)


# It is a custom Filter
class ProductFilter(FilterSet):
    product_id = filters.CharFilter("product_id")
    min_price = filters.CharFilter(label="Min Price", method="min_price_filter")
    max_price = filters.CharFilter(label="Max Price", method="max_price_filter")

    class Meta:
        model = Product
        fields = ('product_id', 'product_name', 'min_price', 'max_price')

    # name is field value
    def min_price_filter(self, queryset, name, value):
        min_price_products = queryset.filter(product_price__gt=value)
        return min_price_products

    def max_price_filter(self, queryset, name, value):
        max_price_products = queryset.filter(product_price__lt=value)
        return max_price_products


class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()
    lookup_field = 'product_id'
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    # use filter field if custom filter class is not present
    # filter_field = ('product_id',)
    filter_class = ProductFilter
    search_fields = ('product_id', 'product_name')
    ordering_fields = ('product_price', 'product_name')

    # It extend the url
    @action(detail=True, methods=['GET'])
    def det(self, request, product_id):
        product = self.get_object()
        invoice_order = InvoiceProduct.objects.filter(item=product)
        serializer = InvoiceProductSerializers(invoice_order, many=True)
        return Response(serializer.data, status=200)


# It only for editing the image. It will not in database.
class UploadView(APIView):
    parser_classes = (FileUploadParser,)
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        file = request.data.get('file', None)
        pdb.set_trace()
        if file:
            return Response({"messsage": "file upload is successfull"}, status=201)
        else:
            return Response({"messsage": "file upload is unsuccessfull"}, status=400)


def about_us(request):
    return render(request, 'aboutus.html')


def send_mail_to(request):
    msg = "Thank you for booking with us. Your booking id "
    # always turn on the less secured app in gmail
    # send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False, )
    send_mail("hey", msg, EMAIL_HOST_USER, ['chaudharypraveen98@gmail.com'], fail_silently=False)
    # messages.success(request, 'Form submission successful')
    return render(request, 'aboutus.html')


class ProductStatisticApi(GenericAPIView):

    def get(self, request, *args, **kwargs):
        invoice_products = InvoiceProduct.objects.filter(item__product_id=kwargs['pk'])
        products = invoice_products
        if invoice_products.count() > 20:
            products = invoice_products[:20]
        order_data = products[:10].values_list('bill_no__invoice_no', 'quantity', 'total')
        x, y, z = zip(*order_data)
        response_data = {
            "quantity": list(map(lambda y: int(y), y)),
            "inv_orders": list(map(lambda x: f'INV{x}', x)),
            "total_price": list(map(lambda z: int(z), z))
        }
        return Response(response_data, status=status.HTTP_200_OK)
