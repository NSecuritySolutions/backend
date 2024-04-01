from rest_framework import serializers
from .models import OurService, Product, OurWorks, Image_Works, Category, ReadySolutions, Manufacturer

class OurServiceListSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)


    class Meta:
        model = OurService
        fields = ['id','image','description']



class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(source='get_category')
    manufacturer = serializers.SerializerMethodField(source='get_manufacturer')


    class Meta:
        model = Product 
        fields = ['id','article', 'model', 'image','description', 'category','manufacturer','resolution', 'dark', \
                  'accommodation','temperature','nutrition', 'microphone', 'micro_sd', \
                    'viewing_angle','focus','price']

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=True).data
    
    def get_manufacturer(self, obj):
        return ManufacturerSerializer(obj.manufacturer, many=True).data

class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    
    class Meta:
        model = Category
        fields = ['id','title']

class ManufacturerSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    
    class Meta:
        model = Manufacturer
        fields = ['id','title']

class ReadySolutionsListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(source='get_product')

    class Meta:
        model = ReadySolutions
        fields = ['id','product']

    def get_product(self, obj):
        return ProductListSerializer(obj.product, many=True).data


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Image_Works
        fields = '__all__'

class OurWorksListSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, required=False)
    description = serializers.CharField(required=True, max_length=500)
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
    