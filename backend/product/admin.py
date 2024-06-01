from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin

from product.models import (
    HDD,
    Camera,
    ImageWorks,
    Manufacturer,
    OurService,
    OurWorks,
    Product,
    ProductCategory,
    ReadySolution,
    Register,
    SolutionToProduct,
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
admin.site.register(HDD)
