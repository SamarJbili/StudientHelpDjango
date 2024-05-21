from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class Post(models.Model):
    OFFRE = 0
    DEMANDE = 1
    TYPE_CHOICES = [
        (OFFRE, 'Offre'),
        (DEMANDE, 'Demande'),
    ]
    Title = models.CharField(max_length=200)
    Type = models.IntegerField(choices=TYPE_CHOICES)
    Date = models.DateTimeField(default=timezone.now)
    Image = models.ImageField(upload_to='media', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    likes = models.IntegerField(default=0)  # Define likes as an IntegerField with a default value of 0
    def image_preview(self):
        if self.Image:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.Image.url))
        else:
            return 'No Image'
    def get_comment_count(self):
        return self.comment_set.count()

    def count_comment(self):
        return self.comment_set.count()
    def count_likes(self):
        return self.like_set.count()

    def count_comments(self):
        return self.comment_set.count()

    class Meta:
        abstract = True
        ordering=['Date']

class Stage(Post):
    OUVRIER = 1
    TECHNICIEN = 2
    PFE = 3
    TYPE_CHOICES = [
        (OUVRIER, 'Ouvrier'),
        (TECHNICIEN, 'Technicien'),
        (PFE, 'Projet de Fin dÉtudes'),
    ]
    Stage_type = models.IntegerField(choices=TYPE_CHOICES)
    Société = models.CharField(max_length=200)
    Durée = models.IntegerField()
    Sujet = models.CharField(max_length=200)
    Contactinfo = models.CharField(max_length=200)
    Spécialité = models.CharField(max_length=100)
    
class Logement(Post):
    Localisation = models.CharField(max_length=200)
    Description = models.TextField()
    Contactinfo = models.CharField(max_length=200)
    
  
class ÉvenClub(Post): 
    Intitulé = models.CharField(max_length=200, default="")
    Description = models.TextField(default="")
    Lieu = models.CharField(max_length=200, default="")
    ContactInfo = models.CharField(max_length=200, default="")
    Club = models.CharField(max_length=100, default="")

class ÉvenSocial(Post):
    Intitulé = models.CharField(max_length=200, default="")
    Description = models.TextField(default="")
    Lieu = models.CharField(max_length=200, default="")
    ContactInfo = models.CharField(max_length=200, default="")
    Prix = models.FloatField(default=0.0)

class Transport(Post):
    Départ = models.CharField(max_length=200)
    Destination = models.CharField(max_length=200)
    Heure_dep = models.TimeField()
    Nbre_sièges = models.IntegerField()
    Contactinfo = models.CharField(max_length=200)

class Recommandation(Post):
    Texte = models.TextField()
    
class Post(Post):
    
    Catg=models.CharField(max_length=200, default="")
    objects = models.Manager()
    

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural='Posts'
        
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)

        
class Like(models.Model):
    
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes",null=True, blank=True)
    class Meta:
        unique_together = ('author', 'post')


class Notification(models.Model):
    LIKE = 'like'
    COMMENT = 'comment'
    # Ajoutez d'autres types de notification au besoin

    TYPE_CHOICES = [
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        # Ajoutez d'autres choix au besoin
    ]

    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    usercom=models.CharField(max_length=200, default="")

    # Utilisez GenericForeignKey pour référencer la publication associée
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-timestamp']
