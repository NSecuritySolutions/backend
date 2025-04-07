from rest_framework import serializers

from main.utils import ParagraphsField
from product.models import (
    ImageWorks,
    Manufacturer,
    NewProduct,
    OurService,
    OurWorks,
    OurWorksProduct,
    ProductCategory,
    ProductProperty,
    ReadySolution,
    SolutionToProduct,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тэгов."""

    class Meta:
        model = Tag
        fields = ("id", "title")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории товаров."""

    class Meta:
        model = ProductCategory
        fields = ("id", "title")


class ManufacturerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели производетеля."""

    class Meta:
        model = Manufacturer
        fields = ("id", "title")


class ProductPropertySerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source="property.field_name")
    name = serializers.CharField(source="property.name")

    class Meta:
        model = ProductProperty
        fields = ("field_name", "name", "value")


class NewProductSerializer(serializers.ModelSerializer):
    properties = ProductPropertySerializer(many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = NewProduct
        fields = "__all__"


class OurServiceListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели наших услуг."""

    description = ParagraphsField()

    class Meta:
        model = OurService
        fields = ("id", "image", "title", "description", "action")


class ProductIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewProduct
        fields = ("id",)

    def to_internal_value(self, data):
        try:
            obj = NewProduct.objects.get(id=data["id"])
            return obj.id
        except NewProduct.DoesNotExist:
            raise serializers.ValidationError(
                f"Product with ID {data['id']} does not exist."
            )


class SolutionToProductSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели готовое решение - товары"""

    product = NewProductSerializer()

    class Meta:
        model = SolutionToProduct
        fields = "__all__"


class ReadySolutionsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели готовых решений."""

    tags = TagSerializer(many=True)
    description = ParagraphsField()
    equipment = SolutionToProductSerializer(many=True)
    equipment_price = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = ReadySolution
        fields = (
            "id",
            "title",
            "image",
            "tooltip_text",
            "description",
            "price",
            "tags",
            "equipment",
            "equipment_price",
        )


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели картинок наших работ."""

    class Meta:
        model = ImageWorks
        fields = ("id", "image", "is_main")


class OurWorksProductSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели наши работы - товары"""

    product = NewProductSerializer()

    class Meta:
        model = OurWorksProduct
        fields = "__all__"


class OurWorksListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели наших работ."""

    images = ImageSerializer(many=True)
    description = ParagraphsField()
    products = OurWorksProductSerializer(many=True)

    class Meta:
        model = OurWorks
        fields = (
            "id",
            "title",
            "images",
            "description",
            "products",
            "time",
            "budget",
            "area",
            "add_date",
        )


class CategoryListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории товаров."""

    children = CategorySerializer(many=True)

    class Meta:
        model = ProductCategory
        fields = ("id", "title", "children")
