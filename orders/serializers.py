from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from users.models import UserProfile

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'items']
        read_only_fields = ['user']

class CheckoutSerializer(serializers.Serializer):
    """
    A simple serializer to validate the checkout request.
    """
    def create(self, validated_data):
        user = self.context['request'].user
        cart = user.cart

        if not cart.items.exists():
            raise serializers.ValidationError("Your cart is empty.")

        # Create a new order for the user
        order = Order.objects.create(user=user)

        # Move items from the cart to the order
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
            item.delete()  # Clear the item from the cart

        return order
