from django.contrib import admin
from .models import Receipt, Tag
# from django.contrib.auth.models import User

# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email')
#     list_filter = ('username', 'email',)

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('creator', 'date')
    list_filter = ('date', 'creator')

class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    list_filter = ('tag',)


# admin.site.register(User, UserAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Tag, TagAdmin)