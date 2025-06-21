from django.contrib import admin
from .models import Class, CustomUser, Journal


class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Пользовательские данные', {'fields': ('username', 'email', 'password',)}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'classID',)}),
        ('Статус', {'fields': ('is_active',)}),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if request.user.is_superuser:
            fieldsets += (
                ('Администрирование', {
                    'fields': ('is_superuser', 'user_permissions', 'is_staff', 'groups'),
                }),
            )
        return fieldsets


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Class)
admin.site.register(Journal)
