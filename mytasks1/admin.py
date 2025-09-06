from django.contrib import admin
from .models import ArchiveItem, MediaFile

class MediaFileInline(admin.TabularInline):
    model = MediaFile
    extra = 1  
    fields = ('file', 'media_type', 'file_name', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

@admin.register(ArchiveItem)
class ArchiveItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_title', 'category', 'content_preview', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'category', 'created_at', 'updated_at')
        }),
        ('Content', {
            'fields': ('content',)
        }),
    )
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [MediaFileInline]
    ordering = ('-created_at',)
    list_per_page = 20

    def short_title(self, obj):
        if len(obj.title) > 30:
            return f"{obj.title[:30]}..."
        return obj.title or "No Title"
    short_title.short_description = "Title"

    def content_preview(self, obj):
        if obj.content:
            return f"{obj.content[:50]}..." if len(obj.content) > 50 else obj.content
        return "-"
    content_preview.short_description = "Content Preview"

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'archive_item_link', 'file_name', 'media_type', 'file_size', 'uploaded_at')
    list_filter = ('media_type', 'uploaded_at')

    search_fields = ('file_name', 'archive_item__title', 'archive_item__content')

    fields = ('archive_item', 'file', 'media_type', 'file_name', 'file_size', 'uploaded_at')

    readonly_fields = ('id', 'uploaded_at', 'file_size')

    ordering = ('-uploaded_at',)


    def archive_item_link(self, obj):
        from django.utils.html import format_html
        return format_html(
            '<a href="/admin/mytasks1/archiveitem/{}/">{}</a>',
            obj.archive_item.id,
            f"{obj.archive_item.title} ({obj.archive_item.category})"
        )
    archive_item_link.short_description = "Archive Item"
    archive_item_link.allow_tags = True  

    def file_size(self, obj):
        try:
            size = obj.file.size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} TB"
        except:
            return "-"
    file_size.short_description = "File Size"
