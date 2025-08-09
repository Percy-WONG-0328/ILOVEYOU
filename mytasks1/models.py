from django.db import models
from django.utils import timezone
import uuid

#这个models还是最初版，没有完善没有integrate，暂时还不能投入使用
class ArchiveItem(models.Model):

    CATEGORY_CHOICES = [
        ('email', 'Email'),
        ('photo', 'Photo'),
        ('message', 'Message'),
        ('emotion', 'Emotion'),
        ('days', 'Days Matter'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="唯一标识符"
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        help_text="项目标题"
    )
    content = models.TextField(
        blank=True,
        help_text="文本内容"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text="项目分类"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="最后更新时间"
    )

    def __str__(self):
        """模型的字符串表示"""
        return f"{self.get_category_display()} - {self.title or 'Untitled'} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        """元数据设置"""
        verbose_name = "Archive Item"
        verbose_name_plural = "Archive Items"
        ordering = ['-created_at']  # 按创建时间倒序排列


class MediaFile(models.Model):
    """媒体文件模型，用于存储图片和音频"""
    
    # 媒体类型选项
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('audio', 'Audio'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    archive_item = models.ForeignKey(
        ArchiveItem,
        on_delete=models.CASCADE,
        related_name='media_files',
        help_text="关联的归档项目"
    )
    file = models.FileField(
        upload_to='archive_media/%Y/%m/%d/',
        help_text="上传的媒体文件"
    )
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
        help_text="媒体类型（图片/音频）"
    )
    uploaded_at = models.DateTimeField(
        default=timezone.now,
        help_text="上传时间"
    )
    file_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="原始文件名"
    )

    def __str__(self):
        return f"{self.get_media_type_display()}: {self.file_name}"

    class Meta:
        verbose_name = "Media File"
        verbose_name_plural = "Media Files"
