from rest_framework import serializers
from .models import *

class OurServiceListSerializer(serializers.Serializer):
    descriptoin = serializers.CharField(required=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)


    class Meta:
        model = OurService
        fields = ['id','image','descriptoin']



class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['model', 'descriptoin', 'category','manufacturer','resolution', 'dark', \
                  'accommodation','temperature','nutrition', 'microphone', 'micro_sd', \
                    'viewing_angle','focus','price']

    
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
    add_date = serializers.DateTimeField(format='%d.%m.%Y')    
    date_works = serializers.DateTimeField(format='%d.%m.%Y')
    price = serializers.IntegerField()
    

    class Meta:
        model = OurWorks
        fields = ['image', 'description', 'add_date', 'date_works', 'price']
