from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin

from application.models import (
    Application,
    ApplicationWithCalculator,
    ApplicationWithFile,
    ApplicationWithSolution,
    TelegramChat,
)


@admin.register(Application)
class ApplicationAdmin(PolymorphicParentModelAdmin):
    base_model = Application
    child_models = (
        ApplicationWithFile,
        ApplicationWithSolution,
        ApplicationWithCalculator,
    )


admin.site.register(ApplicationWithFile)
admin.site.register(ApplicationWithSolution)
admin.site.register(ApplicationWithCalculator)
admin.site.register(TelegramChat)
