from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('model','display_category')
    search_fields = ['model']


admin.site.register(Product, ProductAdmin)
admin.site.register(ReadySolutions)
admin.site.register(OurService)
admin.site.register(OurWorks)
admin.site.register(Category)
admin.site.register(Image_Works)
admin.site.register(Manufacturer)
admin.site.register(Questions)




