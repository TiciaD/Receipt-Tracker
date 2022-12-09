from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.email

class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.date.strftime("%m/%d/%Y")

class Tag(models.Model):
    receipts = models.ManyToManyField(Receipt, blank=True)
    tag = models.CharField(max_length=200)

    def __str__(self):
        return self.tag