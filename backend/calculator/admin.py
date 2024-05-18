from django.contrib import admin
from .models import PriceList, Formula, Calculator, CalculatorBlock, BlockOption


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


admin.site.register(PriceList)
admin.site.register(Formula)
admin.site.register(BlockOption)
