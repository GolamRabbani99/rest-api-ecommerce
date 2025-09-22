from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for creating, viewing, and managing the user's shopping cart.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return the cart for the currently authenticated user.
        """
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Create a new cart and automatically link it to the current user.
        """
        serializer.save(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing items within a user's cart.
    """
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters the queryset to only show items for the specific cart
        referenced in the URL.
        """
        cart_id = self.kwargs['cart_pk']
        return CartItem.objects.filter(cart__id=cart_id, cart__user=self.request.user)

    def perform_create(self, serializer):
        """
        Creates a new cart item and links it to the appropriate cart.
        It also handles adding to the quantity if the product already exists.
        """
        cart_id = self.kwargs['cart_pk']
        cart = Cart.objects.get(id=cart_id, user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # Check if the product is already in the cart
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            serializer.instance = cart_item
        except CartItem.DoesNotExist:
            serializer.save(cart=cart)
