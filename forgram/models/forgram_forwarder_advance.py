from django.db import models
from . import ForGramModel
from accounts.models import User

class ForGramForwarderAdvanceModel(models.Model):
    COMPLETED = 'Completed'
    IN_PROGRESS = 'In Progress'
    NOT_COMPLETED = 'Not Completed'
    
    STATUS_CHOICES = [
        (COMPLETED, 'completed'),
        (IN_PROGRESS, 'in_progress'),
        (NOT_COMPLETED, 'not_completed'),
    ]


    ALLPOST = 'allposts'
    MOMENTARY = 'momentary'
    TYPE_CHOICE = [
        (ALLPOST , 'allposts'),
        (MOMENTARY , 'momentary')
    ]

    forgram = models.ForeignKey(ForGramModel, on_delete=models.CASCADE, related_name='forwarder_advance')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forwarder_advance')
    source_channel = models.CharField(max_length=32, null=True, blank=True)
    destination_channel = models.CharField(max_length=32, null=True, blank=True)
    text_filters = models.JSONField(null=True, blank=True)
    note = models.TextField(null=True , blank=True)
    session_name = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_COMPLETED)
    created = models.DateTimeField(auto_now=True)

    photo = models.BooleanField(default=False, null=True, blank=True)
    audio = models.BooleanField(default=False, null=True, blank=True)
    document = models.BooleanField(default=False, null=True, blank=True)
    sticker = models.BooleanField(default=False, null=True, blank=True)
    video = models.BooleanField(default=False, null=True, blank=True)
    animation = models.BooleanField(default=False, null=True, blank=True)
    voice = models.BooleanField(default=False, null=True, blank=True)
    video_note = models.BooleanField(default=False, null=True, blank=True)

    type = models.CharField(max_length=20 , choices=TYPE_CHOICE ,null=True , blank=True )
    text = models.BooleanField(default=True , null=True , blank=True)
    photo = models.BooleanField(default=True, null=True, blank=True)
    audio = models.BooleanField(default=True, null=True, blank=True)
    document = models.BooleanField(default=True, null=True, blank=True)
    sticker = models.BooleanField(default=True, null=True, blank=True)
    video = models.BooleanField(default=True, null=True, blank=True)
    animation = models.BooleanField(default=True, null=True, blank=True)
    voice = models.BooleanField(default=True, null=True, blank=True)
    video_note = models.BooleanField(default=True, null=True, blank=True)
    pid =models.IntegerField(null=True , blank=True)
    
    def __str__(self) -> str:
        return str(self.user)

    def has_media(self):
        media_fields = [
            'text', 'photo', 'audio', 'document', 'sticker', 'video', 'animation', 'voice', 'video_note'
        ]
        for field in media_fields:
            if getattr(self, field):
                return True
        return False
    
    class Meta :
        ordering = ['-created' ,]
