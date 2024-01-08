from rest_framework import serializers
from .models import Product, Category, PopularSolutions

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(source='get_category')
    material = serializers.SerializerMethodField(source='get_material')

    class Meta:
        model = Product
        fields = ['id','model', 'descriptoin', 'category','material','resolution']

    def get_category(self, obj):
        return CategoryListSerializer(obj.category, many=True).data
    
    def get_material(self, obj):
        return MaterialListSerializer(obj.material, many=True).data
    
class PopularSolutionsListSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField(source='get_product')

    class Meta:
        model = PopularSolutions
        fields = ['id','product']

    def get_product(self, obj):
        return ProductListSerializer(obj.product, many=True).data
    