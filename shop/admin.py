from django.contrib import admin
from .models import Item, Category, SubCategory


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'updated', 'stock', 'available',)
    list_filter = ('category', 'subcategory')
    list_display_links = ('title',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)