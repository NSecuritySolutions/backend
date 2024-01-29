from rest_framework import serializers
from .models import *

class OurServiceListSerializer(serializers.Serializer):
    descriptoin = serializers.CharField(required=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)


    class Meta:
        model = OurService
        fields = ['id','image','descriptoin']



class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(source='get_category')

    class Meta:
        model = Product
        fields = ['model', 'descriptoin', 'category','manufacturer','resolution', 'dark', \
                  'accommodation','temperature','nutrition', 'microphone', 'micro_sd', \
                    'viewing_angle','focus','price']

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=True).data
    

class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    
    class Meta:
        model = Category
        fields = ['title']

class PopularSolutionsListSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField(source='get_product')

    class Meta:
        model = PopularSolutions
        fields = ['id','product']

    def get_product(self, obj):
        return ProductListSerializer(obj.product, many=True).data


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)



class OurWorksListSerializer(serializers.Serializer):
    image = ImageSerializer(many=True, required=False)
    descriptoin = serializers.CharField(required=True)
    product = serializers.SerializerMethodField(source='get_product')
    add_date = serializers.DateTimeField(format='%d.%m.%Y')    
    date_works = serializers.DateTimeField(format='%d.%m.%Y')
    date_finish = serializers.DateTimeField(format='%d.%m.%Y')
    price = serializers.IntegerField()
    

    class Meta:
        model = OurWorks
        fields = ['image', 'description', 'product','add_date', 'date_works', 'date_finish', 'price']

    def get_product(self, obj):
        return ProductListSerializer(obj.product, many=True).data