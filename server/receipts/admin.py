from django.contrib import admin
from .models import Receipt, Tag
# from django.contrib.auth.models import User

# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email')
#     list_filter = ('username', 'email',)

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')
    list_filter = ('date', 'user')

class TagAdmin(admin.ModelAdmin):
    list_display = ('tagName',)
    list_filter = ('tagName',)


# admin.site.register(User, UserAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Tag, TagAdmin)