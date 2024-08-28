from django.db import transaction
from rest_framework import serializers

from application.models import (
    Application,
    ApplicationWithCalculator,
    ApplicationWithFile,
    ApplicationWithSolution,
    CalculatorBlockCategoryProductsData,
    CalculatorBlockData,
    CalculatorData,
    OptionData,
)
from product.models import ReadySolution
from product.serializers import (
    ProductIdSerializer,
    ProductSerializer,
    ReadySolutionsSerializer,
)


class OptionsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionData
        exclude = ("block_data",)


class CategoryProductsSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = CalculatorBlockCategoryProductsData
        exclude = ("block_data",)

    def get_products(self, obj):
        return ProductSerializer(obj.products.all(), many=True, required=False).data

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        products_data = data.get("products", [])
        internal_value["products"] = [
            ProductIdSerializer().to_internal_value({"id": prod["id"]})
            for prod in products_data
        ]
        return internal_value

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        category = CalculatorBlockCategoryProductsData.objects.create(**validated_data)
        category.products.set([prod_id for prod_id in products_data])
        return category

    def create_with_block(self, validated_data, block):
        products_data = validated_data.pop("products")
        category = CalculatorBlockCategoryProductsData.objects.create(
            **validated_data, block_data=block
        )
        if len(products_data) > 0:
            category.products.set([prod_id for prod_id in products_data])
        return category


class BlockDataSerializer(serializers.ModelSerializer):
    products_category = CategoryProductsSerializer(many=True)
    options = OptionsDataSerializer(many=True)

    class Meta:
        model = CalculatorBlockData
        exclude = ("calculator_data",)


class CalculatorDataSerializer(serializers.ModelSerializer):
    blocks = BlockDataSerializer(many=True)

    class Meta:
        model = CalculatorData
        exclude = ("application",)


class ApplicationWithCalcSerializer(serializers.ModelSerializer):
    calculator = CalculatorDataSerializer()

    class Meta:
        model = ApplicationWithCalculator
        exclude = ("polymorphic_ctype",)

    def create(self, validated_data: dict):
        calculator_data = validated_data.pop("calculator")
        with transaction.atomic():
            application = ApplicationWithCalculator.objects.create(**validated_data)
            blocks_data = calculator_data.pop("blocks")
            calculator_object = CalculatorData.objects.create(
                **calculator_data, application=application
            )

            for block_data in blocks_data:
                categories_data = block_data.pop("products_category")
                options_data = block_data.pop("options")
                block_object = CalculatorBlockData.objects.create(
                    **block_data, calculator_data=calculator_object
                )

                for category_data in categories_data:
                    category = CategoryProductsSerializer().create_with_block(
                        category_data, block_object
                    )
                    category.save()

                option_objects = [
                    OptionData(**option_data, block_data=block_object)
                    for option_data in options_data
                ]
                OptionData.objects.bulk_create(option_objects)

        return application


class ApplicationWithFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationWithFile
        exclude = ("polymorphic_ctype",)


class ApplicationWithSolutionSerializer(serializers.ModelSerializer):
    solution = ReadySolutionsSerializer(read_only=True)

    class Meta:
        model = ApplicationWithSolution
        exclude = ("polymorphic_ctype",)


class ApplicationWithSolutionCreateSerializer(serializers.ModelSerializer):
    solution = serializers.PrimaryKeyRelatedField(queryset=ReadySolution.objects.all())

    class Meta:
        model = ApplicationWithSolution
        exclude = ("polymorphic_ctype",)


class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"

    def to_representation(self, instance):
        request = self.context.get("request")
        if isinstance(instance, ApplicationWithFile):
            return ApplicationWithFileSerializer(
                instance, context={"request": request}
            ).data
        elif isinstance(instance, ApplicationWithSolution):
            return ApplicationWithSolutionSerializer(
                instance, context={"request": request}
            ).data
        elif isinstance(instance, ApplicationWithCalculator):
            return ApplicationWithCalcSerializer(
                instance, context={"request": request}
            ).data
        return None
