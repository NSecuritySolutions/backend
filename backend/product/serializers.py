from rest_framework import serializers

from main.utils import ParagraphsField
from product.models import (
    Camera,
    ImageWorks,
    Manufacturer,
    OurService,
    OurWorks,
    Product,
    ProductCategory,
    ReadySolution,
    Register,
    SolutionToProduct,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тэгов."""

    class Meta:
        model = Tag
        fields = ["id", "title"]


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории товаров."""

    class Meta:
        model = ProductCategory
        fields = ["id", "title"]


class ManufacturerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели производетеля."""

    class Meta:
        model = Manufacturer
        fields = ["id", "title"]


class OurServiceListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели наших услуг."""

    description = ParagraphsField()
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

    class Meta:
        model = Register
        exclude = ("polymorphic_ctype", "model")


class CameraSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Camera."""

    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Camera
        exclude = ("polymorphic_ctype", "model")


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


class SolutionToProductSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели готовое решение - товары"""

    product = Product

    class Meta:
        model = SolutionToProduct
        fields = ("id", "solution", "product", "amount")


class ReadySolutionsListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели готовых решений."""

    tags = TagSerializer(many=True)
    description = ParagraphsField()
    equipment = SolutionToProductSerializer(many=True)

    class Meta:
        model = ReadySolution
        fields = [
            "id",
            "title",
            "image",
            "tooltip_text",
            "description",
            "price",
            "tags",
            "equipment",
        ]


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели картинок наших работ."""

    class Meta:
        model = ImageWorks
        fields = ("id", "image", "is_main")


class OurWorksListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели наших работ."""

    images = ImageSerializer(many=True)
    description = ParagraphsField()
    product = ProductListSerializer(many=True)

    class Meta:
        model = OurWorks
        fields = [
            "id",
            "title",
            "images",
            "description",
            "product",
            "time",
            "budget",
            "area",
            "add_date",
        ]
