from django.db import models
from django.conf import settings

class Receipt(models.Model):
    # 'auth.User', related_name='receipts'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    receiptImage = models.ImageField(upload_to='images')
    tags = models.ManyToManyField('Tag')

    class meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.title or ""} {self.date.strftime("%m/%d/%Y")}'


class Tag(models.Model):
    tagName = models.CharField(max_length=255)

    class meta:
        ordering = ['tagName']

    def __str__(self):
        return self.tagName