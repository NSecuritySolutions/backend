from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicInlineSupportMixin,
    PolymorphicParentModelAdmin,
)

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
from product.models import Product


def filter_content_type_for_polymorphic_product():
    product_subclasses = Product.__subclasses__()

    product_models = []
    for subclass in product_subclasses:
        product_models.append(subclass._meta.model_name)

    return ContentType.objects.filter(model__in=product_models)


class PriceInline(admin.StackedInline):
    model = Price


@admin.register(ValueOption)
class ValueOptionAdmin(PolymorphicChildModelAdmin):
    base_model = ValueOption


@admin.register(ProductOption)
class ProductOptionAdmin(PolymorphicChildModelAdmin):
    base_model = ProductOption

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = filter_content_type_for_polymorphic_product()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BlockOption)
class BlockOptionAdmin(PolymorphicParentModelAdmin):
    base_model = BlockOption
    child_models = (ValueOption, ProductOption)


@admin.register(PriceListCategory)
class PriceListCategoryAdmin(admin.ModelAdmin):
    inlines = (PriceInline,)


class PriceListCategoryInline(admin.StackedInline):
    model = PriceListCategory


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    inlines = (PriceListCategoryInline,)


class BlockOptionInline(admin.StackedInline):
    model = BlockOption


class CalculatorBlockInline(admin.TabularInline):
    model = CalculatorBlock


class ProductOptionInline(admin.StackedInline):
    model = ProductOption

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            kwargs["queryset"] = filter_content_type_for_polymorphic_product()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ValueOptionInline(admin.StackedInline):
    model = ValueOption


@admin.register(CalculatorBlock)
class BlockAdmin(admin.ModelAdmin, PolymorphicInlineSupportMixin):
    inlines = (ProductOptionInline, ValueOptionInline)


@admin.register(Calculator)
class CalculatorAdmin(admin.ModelAdmin):
    inlines = (CalculatorBlockInline,)


admin.site.register(Price)
admin.site.register(Formula)
