from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer
from .tasks import send_purchase_confirmation_email

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
        
    def perform_destroy(self, instance):
        instance.delete()

class CartViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def purchase(self, request):
        cart = self.get_queryset().first()
        if not cart:
            return Response({'detail': 'Cart is empty'}, status=400)

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({'detail': 'Cart is empty'}, status=400)

        item_titles = [item.book.title for item in cart_items]
        send_purchase_confirmation_email.delay(request.user.email, item_titles)

        cart_items.delete()  # Clear the cart after purchase
        return Response({
            'detail': 'Purchase completed, confirmation email sent.',
            'items': item_titles
        })

    @action(detail=False, methods=['get'])
    def view_cart_items(self, request):
        cart = self.get_queryset().first()
        if not cart:
            return Response({'detail': 'Cart is empty'}, status=400)

        cart_items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)
