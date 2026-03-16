from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=50, default='Sports')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DietUser(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()
    height = models.IntegerField()   
    weight = models.FloatField()     
    goal = models.CharField(
        max_length=20,
        choices=[
            ('loss', 'Weight Loss'),
            ('gain', 'Muscle Gain'),
            ('maintain', 'Maintain')
        ]
    )

    def __str__(self):
        return self.name


class DietPlan(models.Model):
    GOAL_CHOICES = [
        ('gain', 'Weight Gain'),
        ('loss', 'Weight Loss'),
        ('maintain', 'Maintain Weight'),
    ]

    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    calories = models.IntegerField()
    breakfast = models.TextField()
    lunch = models.TextField()
    dinner = models.TextField()

    def __str__(self):
        return self.goal
    
class Fit(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', default='default_profile.png')

    def __str__(self):
        return self.user.username


