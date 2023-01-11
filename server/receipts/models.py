from django.db import models
from django.contrib.auth.models import User
from .choices import EXPENSE_OPTIONS


class Receipt(models.Model):
    store_name = models.CharField(
        max_length=255, 
        blank=True, 
        null=True
    )
    date = models.DateField()
    expense = models.CharField(max_length=40, choice=EXPENSE_OPTIONS)
    tax = models.DecimalField(
        max_digits=2,
        decimal_places=2,
        blank=True,
        null=True
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        blank=True, 
        null=True
    )
    receipt_image = models.ImageField(
        upload_to='images', 
        blank=True, 
        null=True
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    class meta:
        ordering = ['id']

    def __str__(self):
        if self.store_name:
            return f"{self.store_name} - {self.date}"
        else:
            return f"{self.date}"


class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    class meta:
        ordering = ['tag_name']

    def __str__(self):
        return self.tag_name
