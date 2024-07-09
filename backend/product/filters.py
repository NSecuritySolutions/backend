from django_filters import AllValuesMultipleFilter, FilterSet

from product.models import Product


class ProductFilter(FilterSet):
    category = AllValuesMultipleFilter(field_name="category__title")
    manufacturer = AllValuesMultipleFilter(field_name="manufacturer__title")

    class Meta:
        model = Product
        fields = ["category", "manufacturer"]
