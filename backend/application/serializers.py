from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from application.models import (
    Application,
    ApplicationWithCalculator,
    ApplicationWithFile,
    ApplicationWithSolution,
)
from product.models import ReadySolution
from product.serializers import ProductIdSerializer, ReadySolutionsSerializer


class ApplicationWithFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=False)

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
            return CalculatorJSONSerializer(instance, context={"request": request}).data
        return None


class OptionJSONSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()


class CategoryProductsJSONSerializer(serializers.Serializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    products = ProductIdSerializer(many=True)


class CalculatorBlockJSONSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    amount = serializers.IntegerField()
    products_category = CategoryProductsJSONSerializer(many=True)
    options = OptionJSONSerializer(many=True)


class CalculatorDataJSONSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    blocks = CalculatorBlockJSONSerializer(many=True)


class CalculatorJSONSerializer(serializers.ModelSerializer):
    calculator_data = serializers.JSONField()

    class Meta:
        model = ApplicationWithCalculator
        fields = "__all__"

    def validate_calculator_data(self, value):
        serializer = CalculatorDataJSONSerializer(data=value)
        serializer.is_valid(raise_exception=True)
        return value
