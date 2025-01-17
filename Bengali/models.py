from django.db import models
from django.contrib.auth.models import AbstractUser,Group, Permission


from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


# Create your models here.
class RoleChoices(models.TextChoices):
    ADMIN="admin","admin"
    WORKERS="workers","workers"
    USER="user","user"
    AGENCY="agency","agency"
    

class Profile(AbstractUser):
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()
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
        return self.email


class UserDetails(models.Model):
    profile=models.OneToOneField('Profile',on_delete=models.CASCADE,related_name="user_profile",null=True,blank=True)
    address=models.TextField()
    age=models.IntegerField(blank=True,null=True)
    sex=models.CharField(max_length=10 ,blank=True, null=True)

    def __str__(self):
        return self.address





class WorkersDetails(models.Model):
    profile=models.OneToOneField('Profile',on_delete=models.CASCADE,related_name="worker_profile",null=True,blank=True)
    id_no=models.CharField(max_length=150,null=True)
    image=models.ImageField(null=True , blank=True)
    address=models.TextField()
    age=models.IntegerField(blank=True,null=True)
    gender=models.CharField(max_length=10 ,blank=True, null=True)
    category=models.CharField(max_length=50,blank=True,null=True)

    

    def __str__(self):
        return self.profile.username





class AgencyDetails(models.Model):
     profile=models.OneToOneField('Profile',on_delete=models.CASCADE,related_name="agency_profile",null=True,blank=True)
     agency_name=models.CharField(max_length=150)
     licence_id=models.CharField(max_length=255,null=True)
     address=models.CharField(max_length=140,null=True)
     

     def __str__(self):
        return self.profile.username


class Review(models.Model):
    worker = models.ForeignKey('WorkersDetails', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Review by {self.user.username} for {self.worker.profile.username} - Rating: {self.rating}'
    
    
    
class BookWorker(models.Model):
    worker = models.ForeignKey('WorkersDetails', on_delete=models.CASCADE, related_name='worker_booking')
    user = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='user_booking')
    time = models.TimeField(default=0)
    place = models.TextField(blank=True, null=True)
    additionalnotes = models.CharField(max_length=140,null=True,blank=True)

    def __str__(self):
        return f'booking by {self.user.username} for {self.worker.profile.username} '
    
    
    
    
from django.db import models
from django.utils.timezone import now

class UserComplaints(models.Model):
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
        ("Closed", "Closed"),
    ]

    user = models.ForeignKey( 'UserDetails',on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Open")
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

   




    





        



    