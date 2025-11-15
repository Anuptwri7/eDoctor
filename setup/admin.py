from django.contrib import admin
from django.utils.html import format_html
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'image_preview')
    list_editable = ('is_active',)
    search_fields = ('title',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;width:auto;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"
