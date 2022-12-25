from django.db import models
from django.contrib.auth.models import User

class Receipt(models.Model):
    # 'auth.User', related_name='receipts'
    title = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    receipt_image = models.ImageField(upload_to='images')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    class meta:
        ordering = ['id']

    def __str__(self):
        if self.title:
            return f"{self.title} - {self.date}"
        else:
            return f"{self.date}"


class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    class meta:
        ordering = ['tag_name']

    def __str__(self):
        return self.tagName