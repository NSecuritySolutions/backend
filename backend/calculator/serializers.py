from rest_framework import serializers

from calculator.models import (
    BlockOption,
    Calculation,
    Calculator,
    CalculatorBlock,
    Formula,
    ProductOption,
    ValueOption,
)


class FormulaSerializer(serializers.ModelSerializer):
    """Сериализатор для модели формулы калькулятора."""

    class Meta:
        model = Formula
        fields = "__all__"


class ProductOptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели опции блока калькулятора."""

    dependencies = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = ProductOption
        fields = "__all__"

    def get_dependencies(self, instance: ProductOption) -> bool:
        return instance.dependent.count() > 0

    def get_name(self, instance: ProductOption) -> str:
        if instance.name == "self":
            return f"{instance.name}_{instance.product.pk}"
        return instance.name


class ValueOptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели опции со значениями."""

    dependencies = serializers.SerializerMethodField()

    class Meta:
        model = ValueOption
        fields = "__all__"

    def get_dependencies(self, instance: ValueOption) -> bool:
        return instance.dependent.count() > 0


class OptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели опции блока калькулятора."""

    class Meta:
        model = BlockOption
        fields = "__all__"

    def to_representation(self, instance):
        request = self.context.get("request")
        if isinstance(instance, ValueOption):
            return ValueOptionSerializer(instance, context={"request": request}).data
        elif isinstance(instance, ProductOption):
            return ProductOptionSerializer(instance, context={"request": request}).data
        return None


class CalculationSerializer(serializers.ModelSerializer):
    """Сериализатор для модели расчетов для блока."""

    class Meta:
        model = Calculation
        fields = "__all__"


class BlockSerializer(serializers.ModelSerializer):
    """Сериализатор для модели блока калькулятора."""

    options = OptionSerializer(many=True)
    calculations = CalculationSerializer(many=True)
    formula = FormulaSerializer()

    class Meta:
        model = CalculatorBlock
        fields = "__all__"


class CalculatorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели калькулятора."""

    blocks = BlockSerializer(many=True)

    class Meta:
        model = Calculator
        fields = "__all__"
