from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Member(AbstractUser):
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.username}"
    

def img_validator(image):
    valid_extensions = ['jpg', 'jpeg', 'png']
    ext = image.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError('File type not supported, make sure you are uploading jpg, jpeg, or png.')


class Profile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_imgs', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
