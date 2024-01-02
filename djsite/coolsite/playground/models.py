from django.db import models

# Create your models here.
class InputHistory(models.Model):
    input_text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.input_text
