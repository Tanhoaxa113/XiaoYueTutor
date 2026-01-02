import uuid6
from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.core.models import UUIDModel, TimeStampedModel, StatusModel

# --- 1. ENUMS:
class UserRole(models.TextChoices):
    SU_HUYNH = 'su_huynh', 'Sư Huynh'
    DE_DE = 'de_de', 'Đệ Đệ'
    MUOI_MUOI = 'muoi_muoi', 'Muội Muội'
    TY_TY = 'ty_ty', 'Tỷ Tỷ'

class AiEmotion(models.TextChoices):
    NEUTRAL = 'neutral', 'Bình thường'
    HAPPY = 'happy', 'Vui vẻ'
    SULKING = 'sulking', 'Dỗi'
    ANGRY = 'angry', 'Giận dữ'
    SHY = 'shy', 'Ngại ngùng'

# --- 2. RELATIONSHIP STATE (QUAN TRỌNG NHẤT) ---
class RelationshipState(UUIDModel, TimeStampedModel):
    user_id = models.CharField(max_length=255, db_index=True)
    
    # Cấu hình hiện tại của User (User đang đóng vai gì)
    role = models.CharField(
        max_length=50,
        choices=UserRole.choices,
        default=UserRole.SU_HUYNH
    )
    
    # --- CORE STATS (Cơ chế Unified Core) ---
    # Thang điểm tình cảm (0 - 100).
    affection_score = models.IntegerField(default=50)
    
    # Cấp độ dỗi hiện tại (0-3).
    sulking_level = models.IntegerField(default=0)
    
    # Tổng số lần tương tác (để tính level, mở khóa tính năng sau này)
    interaction_count = models.IntegerField(default=0)
    
    # Bộ nhớ vắn tắt (Summary) về người dùng.
    memory_summary = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Relationship State"
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'role'], 
                name='unique_state_per_role'
            )
        ]
    def __str__(self):
        return f"State of {self.user_id} - Role: {self.current_role} - ♥{self.affection_score}"

# --- 3. SESSION (Được nâng cấp) ---
class ChatSession(UUIDModel, TimeStampedModel):
    # Link về State để biết session này diễn ra trong bối cảnh tình cảm nào
    relationship = models.ForeignKey(
        RelationshipState, 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    user_id = models.CharField(max_length=255, db_index=True)
    session_id = models.CharField(max_length=255, db_index=True, unique=True)
    
    # Snapshot role tại thời điểm tạo session (vì user có thể đổi role sau này)
    role_snapshot = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Session {self.session_id} ({self.role_snapshot})"

# --- 4. MESSAGE (Được nâng cấp) ---
class ChatMessage(TimeStampedModel):
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE, 
        related_name='messages',
        to_field='session_id'
    )
    
    sender = models.CharField(max_length=50) 
    content = models.JSONField(default=dict)
    
    # --- ANALYTICS FIELDS (Tách ra để dễ query) ---

    emotion_snapshot = models.CharField(
        max_length=50, 
        choices=AiEmotion.choices, 
        null=True, blank=True
    )
    
    # Điểm hảo cảm thay đổi sau câu nói này (+5, -10...)
    affection_delta = models.IntegerField(default=0)
    
    # Token tracking
    input_token = models.IntegerField(default=0)
    output_token = models.IntegerField(default=0)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['session', 'timestamp']),
        ]

    def __str__(self):
        return f"[{self.sender}] {self.session_id} ({self.timestamp:%H:%M})"