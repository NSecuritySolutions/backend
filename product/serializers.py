from rest_framework import serializers
from .models import OurService, Product, OurWorks, Image_Works, Category, ReadySolutions, Manufacturer, \
    Questions, Register

class OurServiceListSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)


    class Meta:
        model = OurService
        fields = ['id','image', 'title','description']

class RegisterListSerializer(serializers.ModelSerializer):
    manufacturer = serializers.SerializerMethodField(source='get_manufacturer')


    class Meta:
        model = Register 
        fields = ['id','article', 'model', 'image','description', 'manufacturer','max_resolution', 'quantity_сam', \
                  'quantity_hdd','max_quantity_hdd','nutrition', 'price']

    def get_manufacturer(self, obj):
        return ManufacturerSerializer(obj.manufacturer, many=True).data


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField(source='get_category')
    manufacturer = serializers.SerializerMethodField(source='get_manufacturer')


    class Meta:
        model = Product 
        fields = ['id','article', 'model', 'image','type','description', 'category','manufacturer','resolution', 'dark', \
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
    category = serializers.SerializerMethodField(source='get_category')

    class Meta:
        model = ReadySolutions
        fields = ['id','title','image','description', 'short_description','price', 'category']

    def get_category(self, obj):
        return CategorySerializer(obj.category, many=True).data


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Image_Works
        fields = '__all__'

class OurWorksListSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, required=False)
    date = serializers.DateTimeField(format='%d.%m.%Y')

    class Meta:
        model = OurWorks
        fields = ['id','title', 'main_image', 'image', 'description', 'product', 'deadline', 'budget', 'equipped', 'date']

    def get_product(self, obj):
        return ProductListSerializer(obj.product, many=True).data
    

class QuestionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'