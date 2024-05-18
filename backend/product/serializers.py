from rest_framework import serializers
from .models import (
    OurService,
    Product,
    OurWorks,
    Image_Works,
    Category,
    ReadySolutions,
    Manufacturer,
    Questions,
    Register,
    Camera
)


class CategorySerializer(serializers.ModelSerializer):
    # TODO docstring
    title = serializers.CharField(required=True)

    class Meta:
        model = Category
        fields = ["id", "title"]


class ManufacturerSerializer(serializers.ModelSerializer):
    # TODO docstring
    title = serializers.CharField(required=True)

    class Meta:
        model = Manufacturer
        fields = ["id", "title"]


class OurServiceListSerializer(serializers.ModelSerializer):
    # TODO docstring
    description = serializers.CharField(required=True)
    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )

    class Meta:
        model = OurService
        fields = ["id", "image", "title", "description"]


class RegisterListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Register."""
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()
    # category = serializers.CharField(source="category.title")

    class Meta:
        model = Register
        fields = "__all__"


class CameraSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Camera."""
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Camera
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для моделей унаследованных от Product."""
    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        if isinstance(instance, Camera):
            return CameraSerializer(instance).data
        elif isinstance(instance, Register):
            return RegisterListSerializer(instance).data
        return None

    # def get_content_object(self, obj: P):
    #     if isinstance(obj.content_object, Camera):
    #         return CameraSerializer(obj.content_object).data
    #     elif isinstance(obj.content_object, Register):
    #         return RegisterListSerializer(obj.content_object).data
    #     return None


class ReadySolutionsListSerializer(serializers.ModelSerializer):
    # TODO docstring
    category = CategorySerializer(many=True)

    class Meta:
        model = ReadySolutions
        fields = [
            "id",
            "title",
            "image",
            "description",
            "short_description",
            "price",
            "category",
        ]


class ImageSerializer(serializers.ModelSerializer):
    # TODO docstring
    image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )

    class Meta:
        model = Image_Works
        fields = "__all__"


class OurWorksListSerializer(serializers.ModelSerializer):
    # TODO docstring
    image = ImageSerializer(many=True, required=False)
    date = serializers.DateTimeField(format="%d.%m.%Y")
    product = ProductListSerializer(many=True)

    class Meta:
        model = OurWorks
        fields = [
            "id",
            "title",
            "main_image",
            "image",
            "description",
            "product",
            "deadline",
            "budget",
            "equipped",
            "date",
        ]


class QuestionsListSerializer(serializers.ModelSerializer):
    # TODO docstring
    class Meta:
        model = Questions
        fields = "__all__"
