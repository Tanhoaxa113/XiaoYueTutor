from django.db import models
from django.db.models import F
from uuid6 import uuid7


class TimeStampedModel(models.Model):
    """
    Lớp Trừu tượng dùng cho các Models cần quản lý thời gian:
    - Các thuộc tính:
    + created_at (DateTimeField)
    + updated_at (DateTimeField)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class StatusModel(TimeStampedModel):
    """
    Lớp Trừu tượng dùng cho các Models cần quản lý thời gian, trạng thái, phiên bản:
    - Các thuộc tính:
    + created_at (DateTimeField)
    + updated_at (DateTimeField)
    + is_active (BooleanField)
    + version (PositiveIntegerField)
    """
    is_active = models.BooleanField(default=True)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.version = F('version') + 1
            if 'update_fields' in kwargs and kwargs.get('update_fields'):
                uf = set(kwargs.get('update_fields', []))
                uf.add('version')
                uf.add('updated_at')
                kwargs['update_fields'] = uf

        super().save(*args, **kwargs)
        if not self._state.adding:
            self.refresh_from_db(fields=['version'])

class UUIDModel(StatusModel):
    """
    Lớp Trừu tượng dùng cho các Models cần quản lý thời gian, trạng thái, phiên bản, UUIDV7 làm khóa chính:
    - Các thuộc tính:
    + id (UUIDField)
    + created_at (DateTimeField)
    + updated_at (DateTimeField)
    + is_active (BooleanField)
    + version (PositiveIntegerField)
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid7)

    class Meta:
        abstract = True