from django.db.models import QuerySet
from django_filters import AllValuesMultipleFilter, FilterSet, ModelMultipleChoiceFilter

from product.models import NewProduct, Product, ProductCategory


class ProductFilter(FilterSet):
    manufacturer = AllValuesMultipleFilter(field_name="manufacturer__title")
    category = ModelMultipleChoiceFilter(
        to_field_name="title",
        queryset=ProductCategory.objects.all(),
        method="filter_by_category",
    )

    class Meta:
        model = Product
        fields = ["manufacturer"]

    def filter_by_category(self, queryset: QuerySet[Product], name, value):
        categories = set()
        for category in value:
            categories.update(category.get_descendants(include_self=True))

        if categories:
            return queryset.filter(category__in=categories)
        return queryset


class NewProductFilter(FilterSet):
    manufacturer = AllValuesMultipleFilter(field_name="manufacturer__title")
    category = ModelMultipleChoiceFilter(
        to_field_name="title",
        queryset=ProductCategory.objects.all(),
        method="filter_by_category",
    )

    class Meta:
        model = NewProduct
        fields = ["manufacturer"]

    def filter_by_category(self, queryset: QuerySet[NewProduct], name, value):
        categories = set()
        for category in value:
            categories.update(category.get_descendants(include_self=True))

        if categories:
            return queryset.filter(category__in=categories)
        return queryset
