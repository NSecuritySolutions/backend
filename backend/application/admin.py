from django.contrib import admin
from django.utils.html import format_html
from polymorphic.admin import PolymorphicParentModelAdmin

from application.models import (
    Application,
    ApplicationWithCalculator,
    ApplicationWithFile,
    ApplicationWithSolution,
)


@admin.register(Application)
class ApplicationAdmin(PolymorphicParentModelAdmin):
    base_model = Application
    child_models = (
        ApplicationWithFile,
        ApplicationWithSolution,
        ApplicationWithCalculator,
    )


@admin.register(ApplicationWithCalculator)
class ApplicationWithCalculatorAdmin(admin.ModelAdmin):
    readonly_fields = ["display_calculator_data"]
    list_display = ["name", "email", "phone", "date"]

    def display_calculator_data(self, obj):
        """Отображение связанных данных CalculatorData, блоков и опций"""
        if not obj.calculator:
            return "Нет данных калькулятора"

        calculator_data = obj.calculator
        blocks = calculator_data.blocks.all()

        block_info = ""
        for block in blocks:
            block_info += f"<h4>Блок: {block.name} (Цена: {block.price}, Кол-во: {block.amount})</h4>"

            options = block.options.all()
            if options.exists():
                block_info += "<ul>"
                for option in options:
                    block_info += (
                        f"<li>Опция: {option.name} - Значение: {option.value}</li>"
                    )
                block_info += "</ul>"

            categories = block.products_category.all()
            if categories.exists():
                block_info += "<h5>Категории продуктов:</h5><ul>"
                for category in categories:
                    block_info += f"<li>Категория: {category.name}</li>"
                    products = category.products.all()
                    if products.exists():
                        block_info += "<ul>"
                        for product in products:
                            block_info += f"<li>Товар: {product.model}</li>"
                        block_info += "</ul>"
                block_info += "</ul>"

        return format_html(block_info)

    display_calculator_data.short_description = "Данные калькулятора"


admin.site.register(ApplicationWithFile)
admin.site.register(ApplicationWithSolution)
