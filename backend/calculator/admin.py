from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicInlineSupportMixin,
    PolymorphicParentModelAdmin,
)

from calculator.models import (
    BlockOption,
    Calculation,
    Calculator,
    CalculatorBlock,
    Formula,
    Price,
    PriceList,
    PriceListCategory,
    ProductOption,
    ValueOption,
)


class PriceInline(admin.StackedInline):
    model = Price


@admin.register(ValueOption)
class ValueOptionAdmin(PolymorphicChildModelAdmin):
    base_model = ValueOption


@admin.register(ProductOption)
class ProductOptionAdmin(PolymorphicChildModelAdmin):
    base_model = ProductOption


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


class ValueOptionInline(admin.StackedInline):
    model = ValueOption


class CalculationInline(admin.StackedInline):
    model = Calculation


@admin.register(CalculatorBlock)
class BlockAdmin(admin.ModelAdmin, PolymorphicInlineSupportMixin):
    inlines = (ProductOptionInline, ValueOptionInline, CalculationInline)


@admin.register(Calculator)
class CalculatorAdmin(admin.ModelAdmin):
    inlines = (CalculatorBlockInline,)


admin.site.register(Price)
admin.site.register(Calculation)
admin.site.register(Formula)
