from django.db import models
from authentication.models import User, Address
from product.models import Product
from django.db.models import F


class Order(models.Model):
    STATUS = [
        ('PENDING', 'pending'),
        ('SHIPPED', 'shipped'),
        ('OUT_FOR_DELIVERY', 'out for delivery'),
        ('DELIVERED', 'delivered')
    ]

    MODE = [
        ('CASH_ON_DELIVERY', 'cash on delivery'),
        ('UPI', 'upi'),
        ('DEBIT_CARD', 'debit card')
    ]

    PAY_STATUS = [
        ('NOT_PAID', 'not paid'),
        ('PAID', 'paid')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    status = models.CharField(max_length=30, choices=STATUS, default="PENDING")
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=30, choices=MODE, default="CASH_ON_DELIVERY")
    payment_status = models.CharField(max_length=30, choices=PAY_STATUS, default="NOT_PAID")
    rzp_order_id = models.CharField(max_length=100, null=True, blank=True)

    @property
    def getTotalAmount(self):
        orderItems = OrderItem.objects.filter(order=self.id)
        total = orderItems.aggregate(total=models.Sum(F('product__price')*F('count')))['total']
        return total

    def __str__(self):
        return f'Order({self.id}) | {self.user.email}'

    class Meta:
        db_table = 'order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f'OrderItem({self.id}) -> Order | {self.order.id}'

    class Meta:
        db_table = 'orderitem'
        verbose_name = 'orderitem'
        verbose_name_plural = 'orderitems'


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100)
    razorpay_payment_signature = models.CharField(max_length=500)

