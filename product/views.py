from django.shortcuts import render
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
from product.models import Product, Category, Review
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from authentication.permissions import IsAdminOrReadOnly, IsOwner
from order.models import Order, OrderItem

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly,]


class CategoryViewset(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwner,]

    def create(self, request, *args, **kwargs):
        user = request.user
        prod_id = int(request.data['product'])
        review_exists = self.get_queryset().filter(user=user, product=prod_id).exists()

        if not review_exists:
            order_ids = Order.objects.filter(user=user)
            order_items = OrderItem.objects.filter(order__in=order_ids, product=prod_id).values_list('product', flat=True)
            if prod_id in order_items:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            return Response(data={
                "message": "User haven't placed any order for this product"
            },status=status.HTTP_400_BAD_REQUEST)

        return Response(data={
            "message": "Review already exists for this product by user"
        },status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

