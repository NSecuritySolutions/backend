from django.contrib import admin

from calculator.models import (
    BlockOption,
    Calculator,
    CalculatorBlock,
    Formula,
    Price,
    PriceList,
    PriceListCategory,
)


class PriceInline(admin.StackedInline):
    model = Price


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


@admin.register(CalculatorBlock)
class BlockAdmin(admin.ModelAdmin):
    inlines = (BlockOptionInline,)


@admin.register(Calculator)
class CalculatorAdmin(admin.ModelAdmin):
    inlines = (CalculatorBlockInline,)


admin.site.register(Price)
admin.site.register(Formula)
admin.site.register(BlockOption)
