from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser,BaseUserManager
from pharma_admin.models import ProductItems, Medicines, Ayurveda, Skincare
from django.utils import timezone
from PIL import Image
import pytesseract

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=10,default='')
     # You should use a more secure way to store passwords

    objects = CustomUserManager()
    def __str__(self):
        return self.email

    
class Review(models.Model):
    product = models.ForeignKey(ProductItems, on_delete=models.CASCADE, related_name='reviews',null=True, blank=True)
    medicines = models.ForeignKey(Medicines,on_delete=models.CASCADE, related_name='reviews',null=True, blank=True)
    ayurveda = models.ForeignKey(Ayurveda,on_delete=models.CASCADE, related_name='reviews',null=True, blank=True)
    skincare = models.ForeignKey(Skincare,on_delete=models.CASCADE, related_name='reviews',null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = self.product.prod_name if self.product else 'N/A'
        medicine_name = self.medicines.medicine_name if self.medicines else 'N/A'
        ayurveda_name = self.ayurveda.ayurveda_name if self.ayurveda else 'N/A'
        skincare_name = self.skincare.skincare_name if self.skincare else 'N/A'
        return f"{self.user.username} - {product_name} - {medicine_name} - {ayurveda_name} - {skincare_name} - {self.rating}"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment'] 

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('Health Tips', 'Health Tips'),
        ('Medication Updates', 'Medication Updates'),
        ('Disease Awareness', 'Disease Awareness'),
        ('Research and Development', 'Research and Development'),
        ('Wellness and Fitness', 'Wellness and Fitness'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
class Prescription(models.Model):
    image = models.ImageField(upload_to='prescriptions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def process_image(self):
        image = Image.open(self.image)
        text = pytesseract.image_to_string(image)
        return text
    

class Symptoms_medicine(models.Model):
    symptom = models.CharField(max_length=100)
    medicine_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.symptom}: {self.medicine_name}"
    
class MyOrders(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    items=models.CharField(max_length=1500)
    address=models.TextField()
    quantity=models.CharField(max_length=100)
    price=models.CharField(max_length=100)
    phone_num=models.CharField(max_length=10)
    delivery=models.BooleanField(default=False)
    pending=models.BooleanField(default=False)
   
    def __int__(self):
        return self.id