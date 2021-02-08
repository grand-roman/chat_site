from django.contrib import admin

from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'date', 'author')
    search_fields = ('text',)
    list_filter = ('date',)
    empty_value_display = '-пусто-'


admin.site.register(Message, MessageAdmin)