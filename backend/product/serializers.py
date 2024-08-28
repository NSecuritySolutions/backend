from rest_framework import serializers

from calculator.serializers import PriceSerializer
from main.utils import ParagraphsField
from product.models import (
    FACP,
    HDD,
    Camera,
    ImageWorks,
    Manufacturer,
    OtherProduct,
    OurService,
    OurWorks,
    Product,
    ProductCategory,
    ReadySolution,
    Register,
    Sensor,
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


class OurServiceListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели наших услуг."""

    description = ParagraphsField()

    class Meta:
        model = OurService
        fields = ("id", "image", "title", "description", "action")


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Register."""

    prices_in_price_lists = PriceSerializer(many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Register
        exclude = ("polymorphic_ctype",)


class CameraSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Camera."""

    prices_in_price_lists = PriceSerializer(many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Camera
        exclude = ("polymorphic_ctype",)


class HDDSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Camera."""

    prices_in_price_lists = PriceSerializer(many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = HDD
        exclude = ("polymorphic_ctype",)


class OtherProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели остального товара."""

    prices_in_price_lists = PriceSerializer(many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = OtherProduct
        exclude = ("polymorphic_ctype",)


class FACPSerializer(serializers.ModelSerializer):
    """Сериализатор для модели FACP."""

    prices_in_price_lists = PriceSerializer(many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = FACP
        exclude = ("polymorphic_ctype",)


class SensorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Sensor."""

    prices_in_price_lists = PriceSerializer(many=True)
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Sensor
        exclude = ("polymorphic_ctype",)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для моделей унаследованных от Product."""

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        request = self.context.get("request")
        if isinstance(instance, Camera):
            return CameraSerializer(instance, context={"request": request}).data
        elif isinstance(instance, Register):
            return RegisterSerializer(instance, context={"request": request}).data
        elif isinstance(instance, OtherProduct):
            return OtherProductSerializer(instance, context={"request": request}).data
        elif isinstance(instance, FACP):
            return FACPSerializer(instance, context={"request": request}).data
        elif isinstance(instance, Sensor):
            return SensorSerializer(instance, context={"request": request}).data
        elif isinstance(instance, HDD):
            return HDDSerializer(instance, context={"request": request}).data
        return None


class ProductIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id",)

    def to_internal_value(self, data):
        try:
            obj = Product.objects.get(id=data["id"])
            print(obj)
            return obj.id
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                f"Product with ID {data['id']} does not exist."
            )


class SolutionToProductSerializer(serializers.ModelSerializer):
    """Сериализатор для промежуточной модели готовое решение - товары"""

    product = ProductSerializer()

    class Meta:
        model = SolutionToProduct
        fields = "__all__"


class ReadySolutionsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели готовых решений."""

    tags = TagSerializer(many=True)
    description = ParagraphsField()
    equipment = SolutionToProductSerializer(many=True)

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
        )


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор для модели картинок наших работ."""

    class Meta:
        model = ImageWorks
        fields = ("id", "image", "is_main")


class OurWorksListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели наших работ."""

    images = ImageSerializer(many=True)
    description = ParagraphsField()
    # product = ProductListSerializer(many=True)

    class Meta:
        model = OurWorks
        fields = (
            "id",
            "title",
            "images",
            "description",
            "product",
            "time",
            "budget",
            "area",
            "add_date",
        )
