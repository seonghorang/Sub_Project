from django.db import models

class FrequencyRange(models.Model):
    file_name = models.CharField(max_length=200)
    key = models.CharField(max_length=2, default='C')
