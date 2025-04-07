from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from product.models import (
    ImageWorks,
    Manufacturer,
    NewProduct,
    OurService,
    OurWorks,
    OurWorksProduct,
    ProductCategory,
    ProductProperty,
    ProductType,
    ProductTypeTypeProperty,
    ReadySolution,
    SolutionToProduct,
    Tag,
    TypeProperty,
)


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 0
    can_delete = False
    max_num = 0


@admin.register(NewProduct)
class NewProductAdmin(admin.ModelAdmin):
    base_model = NewProduct
    inlines = (ProductPropertyInline,)
    search_fields = ("category__title", "model", "product_type__name")


class ProductTypeTypePropertyInline(admin.TabularInline):
    model = ProductTypeTypeProperty


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    base_model = ProductType
    inlines = (ProductTypeTypePropertyInline,)


class SolutionToProductInline(admin.TabularInline):
    model = SolutionToProduct


@admin.register(ReadySolution)
class ReadySolutionAdmin(admin.ModelAdmin):
    base_model = ReadySolution
    inlines = (SolutionToProductInline,)
    readonly_fields = ("equipment_price",)

    def equipment_price(self, obj: ReadySolution):
        equipment_price = 0
        for equip in obj.equipment.all():
            if equip.amount and equip.product and equip.product.price:
                equipment_price += equip.amount * equip.product.price
        return equipment_price

    equipment_price.short_description = "Цена оборудования"


class OurWorksProductInline(admin.TabularInline):
    model = OurWorksProduct


class OurWorksImageInline(admin.TabularInline):
    model = ImageWorks


@admin.register(OurWorks)
class OurWorksAdmin(admin.ModelAdmin):
    base_model = OurWorks
    inlines = (OurWorksProductInline, OurWorksImageInline)


admin.site.register(TypeProperty)
admin.site.register(OurService)
admin.site.register(ProductCategory, MPTTModelAdmin)
admin.site.register(Manufacturer)
admin.site.register(Tag)
