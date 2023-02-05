from django.db import models

# Create your models here.
class UserDevice(models.Model):
    farm_id = models.PositiveIntegerField(null=False, blank=False)
    device_id = models.CharField(max_length=200, null=False, blank=False, unique=True)
    device_name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    switch_status = models.BooleanField(null=False, blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'device'
        db_table = 'user_devices'
