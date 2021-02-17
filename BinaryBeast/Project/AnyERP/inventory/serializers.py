from rest_framework import serializers

from bill.models import Product, InvoiceProduct

"""
Read only field in InvoiceProductSerializers will add a extra field response output
It will serialize the InvoiceProducts

"""


class InvoiceProductSerializers(serializers.ModelSerializer):
    date = serializers.ReadOnlyField(source='bill_no.bill_date')

    class Meta:
        model = InvoiceProduct
        ordering = ['-date']
        fields = ('quantity', 'packing', 'bill_no', 'total', 'rate', 'date', 'description')
        # It will also work and includes all the field but we don't want the rate and the item field as they are
        # already present in the product field
        # exclude = []


class ProductInvoiceSerializers(serializers.ModelSerializer):
    invoice_product = InvoiceProductSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('product_id', 'product_name', 'product_price', 'hsn_code', 'invoice_product')
        # for relationship
        # depth = 1
        # exclude = []
        # same here we don't want the igst and sgst and cgst


class ProductSerializers(serializers.ModelSerializer):
    """
    The extra_kwargs works only with HyperlinkedModelSerializer. By default the HyperlinkedRelatedfield assumes the
    view name to be <model_name>-detail and hyperlinkedidentityfield to be <model_name>-detail for standard routers
    tracks = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Object.something,
        read_only=True,
        view_name='track-detail'
    )
    HyperlinkedRelatedField will link all the relationship items
    """
    product_url = serializers.HyperlinkedIdentityField(view_name='api-single-product', lookup_field='pk')

    class Meta:
        model = Product
        # fields = "__all__"
        exclude = ('product_igst', 'product_sgst', 'product_cgst')
        # extra_kwargs = {
        #     'url': {'view_name': 'api-single-product', 'lookup_field': 'pk'},
        # }

    # this is used for saving the data and performing operations on it
    # def validate(self, attrs):
    #     pass
    # def create(self, validated_data):
    #     pass
    # def save(self, **kwargs):
    #     pass
