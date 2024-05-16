from rest_framework import serializers
from .models import PriceList, Formula, Calculator, BlockOption, CalculatorBlock


class PriceListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PriceList."""
    class Meta:
        model = PriceList
        fields = "__all__"


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

    class Meta:
        model = CalculatorBlock
        fields = "__all__"


class CalculatorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели калькулятора."""
    blocks = BlockSerializer(many=True)
    formula = FormulaSerializer()
    price_list = PriceListSerializer()

    class Meta:
        model = Calculator
        fields = "__all__"
