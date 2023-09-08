from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
      class Meta:
            model = Category
            fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
      category = CategorySerializer(read_only=True)
      category_id = serializers.PrimaryKeyRelatedField(
            queryset=Category.objects.all(),
            write_only=True,
            source='category'
      )

      class Meta:
            model = MenuItem
            fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

      def validate_category_id(self, value):
            if not Category.objects.filter(id=value.id).exists():
                  raise serializers.ValidationError('Category does not exist.')
            return value


class CartSerializer(serializers.ModelSerializer):
      class Meta:
            model = Cart
            fields = ['id', 'user', 'menu_item', 'quantity', 'unit_price', 'price']

      def validate_quantity(self, value):
            if value <= 0:
                  raise serializers.ValidationError('Quantity must be a positive integer.')
            return value


class OrderSerializer(serializers.ModelSerializer):
      class Meta:
            model = Order
            fields = ['id', 'user', 'delivery_crew', 'status', 'total']


class OrderItemSerializer(serializers.ModelSerializer):
      class Meta:
            model = OrderItem
            fields = ['id', 'order', 'menu_item', 'quantity', 'unit_price', 'price']
