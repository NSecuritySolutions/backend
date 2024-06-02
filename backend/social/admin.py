from django.contrib import admin

from social.models import Employee, Questions, QuestionsCategory, SocialInfo, Team


class EmployeeInline(admin.TabularInline):
    model = Employee


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = (EmployeeInline,)


admin.site.register(Questions)
admin.site.register(SocialInfo)
admin.site.register(QuestionsCategory)
