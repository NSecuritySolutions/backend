from django.contrib import admin
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
    HDD,
)


class ProductAdmin(admin.ModelAdmin):
    search_fields = ["model"]


admin.site.register(Product, ProductAdmin)
admin.site.register(ReadySolutions)
admin.site.register(OurService)
admin.site.register(OurWorks)
admin.site.register(Category)
admin.site.register(Image_Works)
admin.site.register(Manufacturer)
admin.site.register(Questions)
admin.site.register(Register)
admin.site.register(HDD)
