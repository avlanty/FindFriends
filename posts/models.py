from django.db import models
from users.models import Member

# Create your models here.

class Post(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.username} {self.created_at}" 
    

