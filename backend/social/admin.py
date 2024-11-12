from django.contrib import admin

from social.models import (
    Employee,
    OurGuarantees,
    Questions,
    QuestionsCategory,
    Reviews,
    SocialInfo,
    Subguarantees,
    Team,
)


class SubguaranteesInline(admin.TabularInline):
    model = Subguarantees


class EmployeeInline(admin.TabularInline):
    model = Employee


@admin.register(OurGuarantees)
class OurGuaranteesAdmin(admin.ModelAdmin):
    inlines = (SubguaranteesInline,)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = (EmployeeInline,)


admin.site.register(Subguarantees)
admin.site.register(Employee)
admin.site.register(Questions)
admin.site.register(SocialInfo)
admin.site.register(QuestionsCategory)
admin.site.register(Reviews)
