from django.contrib import admin
from .models import TastyUser


@admin.register(TastyUser)
class UserAdmin(admin.ModelAdmin):
    fields = ('id', 'username', 'avatar')
    list_display = ('id', 'username',)
    search_fields = ('username',)
    readonly_fields = ('username', 'id')
