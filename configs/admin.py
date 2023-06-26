from django.contrib import admin

from configs.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):


    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return not Config.objects.exists()
