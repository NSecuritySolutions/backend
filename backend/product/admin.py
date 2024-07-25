from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from product.models import (
    FACP,
    HDD,
    Camera,
    ImageWorks,
    Manufacturer,
    OurService,
    OurWorks,
    PACSProduct,
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


@admin.register(Camera)
class CameraAdmin(PolymorphicChildModelAdmin):
    base_model = Camera


@admin.register(ReadySolution)
class ReadySolutionAdmin(PolymorphicChildModelAdmin):
    base_model = ReadySolution
    inlines = (SolutionToProductInline,)


@admin.register(Register)
class RegisterAdmin(PolymorphicChildModelAdmin):
    base_model = Register


@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    base_model = Product
    child_models = (Camera, Register)


admin.site.register(OurService)
admin.site.register(OurWorks)
admin.site.register(ProductCategory)
admin.site.register(ImageWorks)
admin.site.register(Manufacturer)
admin.site.register(Tag)
admin.site.register(HDD)
admin.site.register(FACP)
admin.site.register(Sensor)
admin.site.register(PACSProduct)
