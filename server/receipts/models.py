from django.db import models

# Create your models here.

class Receipt(models.Model):
    creator = models.ForeignKey('auth.User', related_name='receipts', on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True, null=True, default='')
    date = models.DateField()
    receiptImage = models.ImageField(upload_to='images')

    class meta:
        ordering = ['title', 'date']

    def __str__(self):
        return f'{self.title or ""} {self.date.strftime("%m/%d/%Y")}'


class Tag(models.Model):
    receipts = models.ManyToManyField(Receipt, blank=True)
    tag = models.CharField(max_length=200)

    class meta:
        ordering = ['tag']

    def __str__(self):
        return self.tag