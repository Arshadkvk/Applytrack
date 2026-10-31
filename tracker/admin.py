from django.contrib import admin

from .models import Application, Contact, Note, StatusChange


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("company", "role", "status", "applied_on", "user")
    list_filter = ("status",)
    search_fields = ("company", "role")


admin.site.register([StatusChange, Contact, Note])
