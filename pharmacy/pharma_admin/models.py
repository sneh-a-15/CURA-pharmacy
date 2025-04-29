from django.db import models
from django.utils import timezone

# Create your models here.
class Medicines(models.Model):
    medicine_name=models.CharField(max_length=250)
    medicine_image=models.ImageField(upload_to="products",blank=True,null=True)
    medicine_price=models.IntegerField()
    medicine_descripton=models.TextField()
    medicine_exp=models.DateField()
    def __str__(self):
        return self.medicine_name


class ProductItems(models.Model):
    prod_name=models.CharField(max_length=250)
    prod_image=models.ImageField(upload_to="products",blank=True,null=True)
    prod_price=models.IntegerField()
    prod_descripton=models.TextField()
    prod_exp=models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.prod_name

class Ayurveda(models.Model):
    med_name=models.CharField(max_length=250)
    med_image=models.ImageField(upload_to="products",blank=True,null=True)
    med_price=models.IntegerField()
    med_descripton=models.TextField()
    med_exp=models.DateField()
    def __str__(self):
        return self.med_name

class Skincare(models.Model):
    skinc_name=models.CharField(max_length=250)
    skinc_image=models.ImageField(upload_to="skincucts",blank=True,null=True)
    skinc_price=models.IntegerField()
    skinc_descripton=models.TextField()
    skinc_exp=models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.skinc_name
    