from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Product)
admin.site.register(PopularSolutions)
admin.site.register(OurService)
admin.site.register(OurWorks)
admin.site.register(Category)
admin.site.register(Image_Works)








