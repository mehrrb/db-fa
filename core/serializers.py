from rest_framework import serializers
from core.models import Category, ProductType, ProductInstance, Recipe, RecipeItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    waste_ratio = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'base_weight', 'waste', 'category', 'category_id', 'unit', 'waste_ratio']

class ProductInstanceSerializer(serializers.ModelSerializer):
    product_type = ProductTypeSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductType.objects.all(),
        source='product_type',
        write_only=True
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = ProductInstance
        fields = [
            'id', 'product_type', 'product_type_id', 'total_weight', 'price_per_kilo', 
            'unit', 'waste_weight', 'net_weight', 'total_price', 'created_at', 'user'
        ]
        read_only_fields = ['waste_weight', 'net_weight', 'total_price', 'created_at']
    
    def create(self, validated_data):
        # Set the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class RecipeItemSerializer(serializers.ModelSerializer):
    product_instance = ProductInstanceSerializer(read_only=True)
    product_instance_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductInstance.objects.all(),
        source='product_instance',
        write_only=True
    )
    
    class Meta:
        model = RecipeItem
        fields = ['id', 'product_instance', 'product_instance_id', 'quantity']

class RecipeSerializer(serializers.ModelSerializer):
    recipe_items = RecipeItemSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    profit = serializers.SerializerMethodField()
    profit_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'description', 'created_at', 'user', 
            'total_cost', 'selling_price', 'recipe_items', 
            'profit', 'profit_percentage'
        ]
        read_only_fields = ['created_at', 'total_cost']
    
    def create(self, validated_data):
        # Set the current user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def get_profit(self, obj):
        return obj.calculate_profit()
    
    def get_profit_percentage(self, obj):
        return obj.calculate_profit_percentage() 