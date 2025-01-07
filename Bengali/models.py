from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission

# Create your models here.
class RoleChoices(models.TextChoices):
    ADMIN="admin","admin"
    WORKERS="workers","workers"
    USER="user","user"
    AGENCY="agency","agency"
    

class Profile(AbstractUser):
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]

    username = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name= models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=15,choices=RoleChoices.choices)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField( 
        Group,
            related_name="profile_groups",  # Set unique related_name
            blank=True
        )
    user_permissions = models.ManyToManyField(
            Permission,
            related_name="profile_permissions",  # Set unique related_name
            blank=True
        )

    def __str__(self):
        return self.username


class UserDetails(models.Model):
    profile=models.OneToOneField('Profile',on_delete=models.CASCADE,related_name="user_profile",null=True,blank=True)
    address=models.TextField()
    age=models.IntegerField(blank=True,null=True)
    sex=models.CharField(max_length=10 ,blank=True, null=True)

    def __str__(self):
        return self.profile.username





class WorkersDetails(models.Model):
    profile=models.OneToOneField('Profile',on_delete=models.CASCADE,related_name="worker_profile",null=True,blank=True)
    id_no=models.CharField(max_length=150,null=True)
    image=models.ImageField(null=True , blank=True)
    time=models.TimeField()
    amount=models.IntegerField()
    address=models.TextField()
    
    

    def __str__(self):
        return self.profile.username





class AgencyDetails(models.Model):
     profile=models.OneToOneField('Profile',on_delete=models.CASCADE,related_name="agency_profile",null=True,blank=True)
     Agency_Name=models.CharField(max_length=150)
     licence_id=models.IntegerField(null=True)
     address=models.CharField(max_length=140,null=True)
     

     def __str__(self):
        return self.profile.username




        



    