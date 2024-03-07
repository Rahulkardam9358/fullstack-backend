from rest_framework import serializers
from authentication.serializers import AddressSerializer
from order.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['order']
        extra_kwargs = {
            'order': {
                'required': False,
                'read_only': True,
                'allow_null': True
            },
            'product': {
                'required': False,
                'read_only': True,
                'allow_null': True
            }
        }


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, required=False, read_only=True, allow_null=True)
    item_order = OrderItemSerializer(many=True, required=False, read_only=True, allow_null=True)
    total_amount = serializers.ReadOnlyField(source='getTotalAmount')

    class Meta:
        model = Order
        exclude = ['user']