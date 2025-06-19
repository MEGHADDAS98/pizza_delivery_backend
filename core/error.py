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

class PizzaRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pizza = models.ForeignKey('Pizza', on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# core/serializers.py
from .models import Order, OrderItem, PizzaRating
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

class PizzaRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaRating
        fields = ['id', 'pizza', 'rating', 'comment', 'created_at']


# core/views.py (append this)
from .models import PizzaRating, Pizza
from .serializers import PizzaRatingSerializer

class PizzaRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = PizzaRatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        pizza_id = request.query_params.get('pizza_id')
        if pizza_id:
            ratings = PizzaRating.objects.filter(pizza_id=pizza_id)
        else:
            ratings = PizzaRating.objects.all()
        serializer = PizzaRatingSerializer(ratings, many=True)
        return Response(serializer.data)


# core/urls.py (append this)
from .views import PizzaRatingView

urlpatterns += [
    path('rate-pizza/', PizzaRatingView.as_view(), name='pizza-rating'),
]
