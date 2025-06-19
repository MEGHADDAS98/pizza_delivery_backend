from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .models import Pizza, Cart, CartItem, Order, OrderItem, DeliveryComment, Rating

admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryComment)
admin.site.register(Rating)


admin.site.register(CustomUser, UserAdmin)
