from django.db import models

class UserInfo(models.Model):
    user_seq = models.AutoField(primary_key=True)
    birth = models.DateField()
    id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    profile_url = models.CharField(max_length=255)
    role = models.CharField(max_length=6, choices=[('ADMIN', 'Admin'), ('SENIOR', 'Senior'), ('YOUTH', 'Youth')])
    sex = models.CharField(max_length=255)
    age = models.IntegerField()
    location = models.CharField(max_length=255)
    interest = models.CharField(max_length=255)
    personality = models.CharField(max_length=255)
    career = models.CharField(max_length=255)
    hobby = models.CharField(max_length=255)

    class Meta:
        db_table = 'user_info'

    def __str__(self):
        return self.name
    
class UserEmbedding(models.Model):
    user_info = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    location_embedding = models.JSONField()
    career_embedding = models.JSONField()
    hobby_embedding = models.JSONField()
    interest_embedding = models.JSONField()
    personality_embedding = models.JSONField()
    
    #def __str__(self):
    #    return f'Embeddings for user: {self.user_info.id}'
