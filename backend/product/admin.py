from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from polymorphic.admin import PolymorphicParentModelAdmin

from product.models import (
    FACP,
    HDD,
    Camera,
    ImageWorks,
    Manufacturer,
    OtherProduct,
    OurService,
    OurWorks,
    OurWorksProduct,
    Product,
    ProductCategory,
    ReadySolution,
    Register,
    Sensor,
    SolutionToProduct,
    Tag,
)


class SolutionToProductInline(admin.TabularInline):
    model = SolutionToProduct


@admin.register(ReadySolution)
class ReadySolutionAdmin(admin.ModelAdmin):
    base_model = ReadySolution
    inlines = (SolutionToProductInline,)


class OurWorksProductInline(admin.TabularInline):
    model = OurWorksProduct


@admin.register(OurWorks)
class OurWorksAdmin(admin.ModelAdmin):
    base_model = OurWorks
    inlines = (OurWorksProductInline,)


@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    base_model = Product
    child_models = (Camera, Register, FACP, Sensor, OtherProduct, HDD)
    search_fields = ("category__title", "model")


admin.site.register(OurService)
admin.site.register(ProductCategory, MPTTModelAdmin)
admin.site.register(ImageWorks)
admin.site.register(Manufacturer)
admin.site.register(Tag)
admin.site.register(Camera)
admin.site.register(Register)
admin.site.register(FACP)
admin.site.register(Sensor)
admin.site.register(OtherProduct)
admin.site.register(HDD)
