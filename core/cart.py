from .models import Cart, CartItem, Pizza
from rest_framework import serializers

class CartItemSerializer(serializers.ModelSerializer):
    pizza = serializers.StringRelatedField()  # shows pizza name instead of ID

    class Meta:
        model = CartItem
        fields = ['id', 'pizza', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']

#VIEW

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Pizza
from .serializers import CartSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        pizza_id = request.data.get('pizza_id')
        quantity = request.data.get('quantity', 1)

        if not pizza_id:
            return Response({'error': 'pizza_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pizza = Pizza.objects.get(id=pizza_id)
        except Pizza.DoesNotExist:
            return Response({'error': 'Pizza not found'}, status=status.HTTP_404_NOT_FOUND)

        cart = self.get_cart(request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)
        item.quantity += int(quantity)
        item.save()
        return Response({'message': 'Pizza added to cart'}, status=status.HTTP_200_OK)

    def delete(self, request):
        cart = self.get_cart(request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'}, status=status.HTTP_200_OK)

#URLS

from .views import CartView

urlpatterns += [
    path('cart/', CartView.as_view(), name='cart'),
]
