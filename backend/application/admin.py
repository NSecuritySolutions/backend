from django.contrib import admin
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
