from django.contrib import admin

from calculator.models import (
    BlockOption,
    Calculator,
    CalculatorBlock,
    Formula,
    Price,
    PriceList,
)


class PriceInline(admin.StackedInline):
    model = Price


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    inlines = (PriceInline,)


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


admin.site.register(Formula)
admin.site.register(BlockOption)
