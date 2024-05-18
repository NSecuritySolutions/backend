from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from .models import (
    Product,
    ReadySolutions,
    OurService,
    OurWorks,
    Category,
    Image_Works,
    Manufacturer,
    Questions,
    Register,
    Camera,
    HDD,
)


@admin.register(Camera)
class CameraAdmin(PolymorphicChildModelAdmin):
    base_model = Camera


@admin.register(Register)
class RegisterAdmin(PolymorphicChildModelAdmin):
    base_model = Register


@admin.register(Product)
class ProductAdmin(PolymorphicParentModelAdmin):
    base_model = Product
    child_models = (Camera, Register)


admin.site.register(ReadySolutions)
admin.site.register(OurService)
admin.site.register(OurWorks)
admin.site.register(Category)
admin.site.register(Image_Works)
admin.site.register(Manufacturer)
admin.site.register(Questions)
admin.site.register(HDD)
