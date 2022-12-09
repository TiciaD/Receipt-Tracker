from django.contrib import admin
from .models import User, Receipt, Tag

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    list_filter = ('email',)

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    list_filter = ('date',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    list_filter = ('tag',)


admin.site.register(User, UserAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Tag, TagAdmin)