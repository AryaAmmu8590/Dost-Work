from django.db import models

# Create your models here.

class gender1(models.TextChoices):
    MALE="Male", "Male" 
    FEMALE="FEMALE" ,"FEMALE"

 #model(User_reg)

class User_reg(models.Model):
    phone=models.CharField(max_length=10, null=True)
    address=models.TextField()
    gender=models.CharField(max_length=10,choices=gender1.choices)


    def __str__(self):
        return f'user {self.id}'


    
    





