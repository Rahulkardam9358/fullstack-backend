from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets, status
from rest_framework.response import Response
from math import ceil
import razorpay
from django.conf import settings
from math import ceil
from order.models import Order
from order.serializers import OrderSerializer, OrderItemSerializer
from authentication.models import Address
from authentication.serializers import AddressSerializer
from product.models import Product


client = razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID, 
        settings.RAZORPAY_KEY_SECRET
    )
)

# Create your views here.

class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        '''It axpect the post data in below format
        {
            "name": "name on billing",
            "payment_mode": "CASH_ON_DELIVERY",
            "items":[
                {
                    "id": 1,
                    "count": 2
                }
            ],
            "address": {
                "exist": false,
                "addressData": {
                    "address_line1": "1419, Adarsh nagar colony",
                    "address_line2": "Dastoi marg",
                    "city": "Hapur",
                    "postal_code": "245101",
                    "state": "Uttar Pradesh",
                    "country": "India",
                    "mobile": "India"
                }
            }
        }
        '''

        postdata = request.data
        if postdata['address']['exist']:
            '''we will verify if address belongs to logged in user or not'''
            addressId = postdata['address']['addressId']
            address = Address.objects.get(id=addressId)
            if address.user.email == request.user.email:
                return self.generateOrder(request, address)

            return Response(data={
                "message": "Address does not belong to logged in user"
            },status=status.HTTP_400_BAD_REQUEST)

        addressData = postdata['address']['addressData']
        addressSerializer = AddressSerializer(data=addressData)
        addressSerializer.is_valid(raise_exception=True)
        addressSerializer.save(user=request.user)
        address = Address.objects.get(id=addressSerializer.data['id'])
        orderData = self.generateOrder(request, address)
        order = Order.objects.get(id=orderData['id'])
        # Here we will add code to generate razorpay order and keep id in Order model
        rzp_data = {
            'amount': ceil(order.getTotalAmount),
            'currency': 'INR',
            'payment_capture': 0
        }
        response = client.order.create(data=rzp_data)
        order.rzp_order_id = response['id']
        order.save()
        return Response(data=orderData,status=status.HTTP_201_CREATED)

    def generateOrder(self, request, address):
        postdata = request.data
        orderData = {
            "name": postdata['name'],
            "payment_mode": postdata['payment_mode']
        }
        orderSerializer = self.get_serializer(data=orderData)
        orderSerializer.is_valid(raise_exception=True)
        orderSerializer.save(user=request.user, address=address)
        orderId = orderSerializer.data['id']
        order = Order.objects.get(id=orderId)
        for item in postdata['items']:
            itemData = {
                'count': item['count']
            }
            product = Product.objects.get(id=item['id'])
            itemSerializer = OrderItemSerializer(data=itemData)
            itemSerializer.is_valid(raise_exception=True)
            itemSerializer.save(order=order, product=product)
        return orderSerializer.data


class PaymentHandler(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        params_dict = {
            'razorpay_order_id': request.POST.get('order_id'),
            'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
            'razorpay_signature': request.POST.get('razorpay_signature')
        }
        res = client.utility.verify_payment_signature(params_dict)
        if res:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(data={'message': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST, headers=headers)

