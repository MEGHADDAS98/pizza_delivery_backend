Perfect — I’ve aligned the models in your document to match what you pasted, and slightly updated the `Rating` model to include:

* `related_name='ratings'` (helps when querying `pizza.ratings.all()`)
* `created_at = models.DateTimeField(auto_now_add=True)` (for ordering/sorting)

---

### ✅ Next Step: Hook the Rating API

Now that your model is in shape, let’s wire up the actual endpoint.

---

### 1. **Add the Serializer**

```python
# core/serializers.py

from .models import Rating
from rest_framework import serializers

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'pizza', 'rating', 'comment', 'created_at']
```

---

### 2. **Add the API View**

```python
# core/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Rating
from .serializers import RatingSerializer

class RatingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = RatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        pizza_id = request.query_params.get('pizza_id')
        ratings = Rating.objects.filter(pizza_id=pizza_id) if pizza_id else Rating.objects.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)
```

---

### 3. **Add to URL Patterns**

```python
# core/urls.py

from .views import RatingView

urlpatterns += [
    path('rate-pizza/', RatingView.as_view(), name='rate-pizza'),
]
```

---

### 🔍 Try in Postman

**POST**:
`http://127.0.0.1:8000/api/rate-pizza/`
Headers:
`Authorization: Bearer <access_token>`
`Content-Type: application/json`

Body:

```json
{
  "pizza": 1,
  "rating": 5,
  "comment": "Best crust ever!"
}
```

Let me know when this works — or if you'd like to sort/filter average ratings per pizza next 🔥



# core/models.py
from django.db import models
from django.conf import settings

# Pizza model
class Pizza(models.Model):
    PIZZA_TYPE_CHOICES = (
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(max_length=10, choices=PIZZA_TYPE_CHOICES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Cart model
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# Order model
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='deliveries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

# DeliveryComment model
class DeliveryComment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Rating model
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
