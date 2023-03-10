from django.db import models

# Create your models here.
class Farm(models.Model):
    user_id = models.PositiveIntegerField(null=False, blank=False)
    farm_name = models.CharField(max_length=100, null=False, blank=False)
    address = models.TextField(null=True, blank=True)
    longtude = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'farm'
        db_table = 'user_farms'
