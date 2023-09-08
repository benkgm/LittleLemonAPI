# Import necessary modules and classes
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework import status

# Define a view for menu items that can handle GET and POST requests
@api_view(['GET', 'POST'])
def menu_items_view(request):
    # If the request method is GET, retrieve menu items based on query parameters
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        per_page = request.query_params.get('perpage', default=6)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title__istartswith=search)
        if ordering:
            items = items.order_by(ordering)
        paginator = Paginator(items, per_page=per_page)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)
    # If the request method is POST, create a new menu item
    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)

# Define a view for a single menu item that can handle GET, POST, PUT, and DELETE requests
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def single_menu_item_view(request, id):
    item = MenuItem.objects.get(pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

# Define a view for the cart that can handle GET, POST, PUT, and DELETE requests
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def cart_view(request):
    cart = Cart.objects.all()
    serialized_cart = CartSerializer(cart, many=True)
    return Response(serialized_cart.data)

# Define a view for orders that can handle GET, POST, PUT, and DELETE requests
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def orders_view(request):
    order = Order.objects.all()
    serialized_order = OrderSerializer(order, many=True)
    return Response(serialized_order.data)

# Define a view for order items that can handle GET and POST requests
@api_view(['GET', 'POST'])
def order_items_view(request):
    items = MenuItem.objects.all()
    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data, safe=False)

# Define a view for a secret message that requires authentication
@api_view()
@permission_classes([IsAuthenticated])
def secret_view(request):
    return Response({'message': 'Secret message'})

# Define a view for manager access that requires authentication and manager group membership
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({'message': 'Manager access'})
    else:
        return Response({'message': 'You are not authorized'}, status=status.HTTP_400_BAD_REQUEST)

# Define a view for checking the anonymous rate throttle
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check_view(request):
    return Response({'message': 'Successful'}, status=status.HTTP_200_OK)

# Define a view for checking the user rate throttle
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth_view(request):
    return Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
@permission_classes([IsAdminUser])
def managers_view(request):
    username = request.data.get('username')
    if username:
        user = User.objects.get(username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({'message': 'Access ok'}, status=status.HTTP_200_OK)

    return Response({'message': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

    