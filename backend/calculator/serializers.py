from rest_framework import serializers

from calculator.models import (
    BlockOption,
    Calculator,
    CalculatorBlock,
    Formula,
    Price,
    PriceList,
)


class PriceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели цены."""

    class Meta:
        model = Price
        fields = "__all__"


class PriceListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PriceList."""

    prices = PriceSerializer(many=True)

    class Meta:
        model = PriceList
        fields = "__all__"


class PriceListCalculatorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PriceList."""

    prices = PriceSerializer(many=True)

    class Meta:
        model = PriceList
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        fields = data.get("prices", [])
        result = {field["variable_name"]: field["price"] for field in fields}
        return result


class FormulaSerializer(serializers.ModelSerializer):
    """Сериализатор для модели формулы калькулятора."""

    class Meta:
        model = Formula
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели опции блока калькулятора."""

    class Meta:
        model = BlockOption
        fields = "__all__"


class BlockSerializer(serializers.ModelSerializer):
    """Сериализатор для модели блока калькулятора."""

    options = OptionSerializer(many=True)
    formula = FormulaSerializer()

    class Meta:
        model = CalculatorBlock
        fields = "__all__"


class CalculatorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели калькулятора."""

    blocks = BlockSerializer(many=True)
    price_list = PriceListCalculatorSerializer()

    class Meta:
        model = Calculator
        fields = "__all__"
