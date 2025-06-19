# core/models.py
from django.db import models
from django.conf import settings

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('online', 'Online')])
    delivery_status = models.CharField(max_length=20, default='Pending')
    delivery_comment = models.TextField(blank=True, null=True)
    delivery_partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    pizza = models.ForeignKey('Pizza', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


# core/serializers.py
from .models import Order, OrderItem
from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['pizza', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'payment_method', 'delivery_status', 'delivery_comment', 'items']


# core/views.py (append this)
from rest_framework.views import APIView
from .models import Order, OrderItem, Cart, CartItem, CustomUser
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import random

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_method = request.data.get('payment_method')
        if payment_method not in ['cash', 'online']:
            return Response({'error': 'Invalid payment method'}, status=400)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        if not cart_items:
            return Response({'error': 'Cart is empty'}, status=400)

        with transaction.atomic():
            total_price = sum(item.pizza.price * item.quantity for item in cart_items)
            delivery_partners = CustomUser.objects.filter(role='delivery')
            delivery_partner = random.choice(delivery_partners) if delivery_partners else None

            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                payment_method=payment_method,
                delivery_partner=delivery_partner
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    pizza=item.pizza,
                    quantity=item.quantity
                )
            cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=201)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class DeliveryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, delivery_partner=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or not assigned to you'}, status=404)

        order.delivery_status = request.data.get('delivery_status', order.delivery_status)
        order.delivery_comment = request.data.get('delivery_comment', order.delivery_comment)
        order.save()
        return Response({'message': 'Delivery updated'})


# core/urls.py (append this)
from .views import CheckoutView, OrderListView, DeliveryUpdateView

urlpatterns += [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('delivery/<int:order_id>/', DeliveryUpdateView.as_view(), name='delivery-update'),
]
