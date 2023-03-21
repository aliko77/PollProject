from django.contrib import admin
from .models import Poll


# Register your models here.

class PollAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "slug"]
    readonly_fields = ["slug"]


admin.site.register(Poll, PollAdmin)
