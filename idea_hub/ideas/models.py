from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

class Idea(models.Model):
    STAGE_CHOICES = [
        ('brain_spark', '💡 Brain Spark'),
        ('rough_sketch', '📝 Rough Sketch'),
        ('proto_play', '🔧 Proto Play'),
        ('market_snoop', '🕵️ Market Snoop'),
        ('go_mode', '🚀 Go Mode'),
    ]
    
    # Other fields remain the same
    name = models.CharField(max_length=255)
    elevator_pitch = models.TextField()
    industry = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    description = models.TextField()
    tags = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    funding_status = models.BooleanField(default=False)
    looking_for_funding = models.BooleanField(default=False)
    hiring_status = models.BooleanField(default=False)
    paying_status = models.BooleanField(default=False)
    team_size = models.IntegerField()

    # Multiple owners for an idea
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='owned_ideas')

    def __str__(self):
        return self.name