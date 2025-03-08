from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from main.utils import ParagraphsField
from product.models import (
    FACP,
    HDD,
    Camera,
    ImageWorks,
    Manufacturer,
    NewProduct,
    OtherProduct,
    OurService,
    OurWorks,
    OurWorksProduct,
    Product,
    ProductCategory,
    ProductProperty,
    ReadySolution,
    Register,
    Sensor,
    SolutionToProduct,
    Tag,
)


@extend_schema_field(
    {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "value": {
                    "oneOf": [
                        {"type": "string"},
                        {"type": "boolean"},
                        {"type": "integer"},
                    ]
                },
            },
        },
    }
)
def form_properties(instance):
    data = [
        field.name
        for field in instance._meta.get_fields()
        if not field.is_relation and not field.many_to_one and not field.one_to_one
    ]
    return [
        {
            "name": instance._meta.get_field(field).verbose_name,
            "value": getattr(instance, field),
        }
        for field in data
        if field
        not in (
            "id",
            "model",
            "created_at",
            "updated_at",
            "price",
            "description",
            "manufacturer",
            "category",
            "image",
            "tooltip",
            "properties",
            "polymorphic_ctype",
        )
    ]


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


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Register."""

    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

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


class HDDSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Camera."""

    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = HDD
        fields = "__all__"


class OtherProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели остального товара."""

    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = OtherProduct
        fields = "__all__"


class FACPSerializer(serializers.ModelSerializer):
    """Сериализатор для модели FACP."""

    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = FACP
        fields = "__all__"


class SensorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Sensor."""

    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Sensor
        fields = "__all__"


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


class RegisterRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product с properties в виде списка объектов."""

    properties = serializers.SerializerMethodField()
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Register
        fields = "__all__"

    def get_properties(self, instance):
        return form_properties(instance)


class CameraRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Camera с properties в виде списка объектов."""

    properties = serializers.SerializerMethodField()
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Camera
        fields = "__all__"

    def get_properties(self, instance):
        return form_properties(instance)


class HDDRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для модели HDD с properties в виде списка объектов."""

    properties = serializers.SerializerMethodField()
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = HDD
        fields = "__all__"

    def get_properties(self, instance):
        return form_properties(instance)


class OtherProductRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для модели OtherProduct с properties в виде списка объектов."""

    properties = serializers.SerializerMethodField()
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = OtherProduct
        fields = "__all__"

    def get_properties(self, instance):
        return form_properties(instance)


class FACPRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для модели FACP с properties в виде списка объектов."""

    properties = serializers.SerializerMethodField()
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = FACP
        fields = "__all__"

    def get_properties(self, instance):
        return form_properties(instance)


class SensorRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Sensor с properties в виде списка объектов."""

    properties = serializers.SerializerMethodField()
    category = CategorySerializer()
    manufacturer = ManufacturerSerializer()

    class Meta:
        model = Sensor
        fields = "__all__"

    def get_properties(self, instance):
        return form_properties(instance)


class ProductRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для моделей унаследованных от Product."""

    class Meta:
        model = Product
        fields = "__all__"

    def to_representation(self, instance):
        request = self.context.get("request")
        if isinstance(instance, Camera):
            return CameraRetrieveSerializer(instance, context={"request": request}).data
        elif isinstance(instance, Register):
            return RegisterRetrieveSerializer(
                instance, context={"request": request}
            ).data
        elif isinstance(instance, OtherProduct):
            return OtherProductRetrieveSerializer(
                instance, context={"request": request}
            ).data
        elif isinstance(instance, FACP):
            return FACPRetrieveSerializer(instance, context={"request": request}).data
        elif isinstance(instance, Sensor):
            return SensorRetrieveSerializer(instance, context={"request": request}).data
        elif isinstance(instance, HDD):
            return HDDRetrieveSerializer(instance, context={"request": request}).data
        return None


class CategoryListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории товаров."""

    children = CategorySerializer(many=True)

    class Meta:
        model = ProductCategory
        fields = ("id", "title", "children")
