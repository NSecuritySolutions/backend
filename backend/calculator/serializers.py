from rest_framework import serializers

from calculator.models import (
    BlockOption,
    Calculator,
    CalculatorBlock,
    Formula,
    Price,
    PriceList,
    PriceListCategory,
    ProductOption,
    ValueOption,
)


class PriceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели цены."""

    class Meta:
        model = Price
        fields = "__all__"


class PriceListCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категории прайс листа."""

    prices = PriceSerializer(many=True)

    class Meta:
        model = PriceListCategory
        fields = "__all__"


class PriceListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PriceList."""

    categories = PriceListCategorySerializer(many=True)

    class Meta:
        model = PriceList
        fields = "__all__"


class PriceListCalculatorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели PriceList."""

    # prices = PriceSerializer(many=True)
    categories = PriceListCategorySerializer(many=True)

    class Meta:
        model = PriceList
        fields = "__all__"

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     fields = data.get("prices", [])
    #     result = {field["variable_name"]: field["price"] for field in fields}
    #     return result


class FormulaSerializer(serializers.ModelSerializer):
    """Сериализатор для модели формулы калькулятора."""

    class Meta:
        model = Formula
        fields = "__all__"


class ProductOptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели опции блока калькулятора."""

    dependencies = serializers.SerializerMethodField()

    class Meta:
        model = ProductOption
        fields = "__all__"

    def get_dependencies(self, instance: ProductOption) -> bool:
        return instance.dependent.count() > 0


class ValueOptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели опции со значениями."""

    price = PriceSerializer()
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
