from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    rating = models.IntegerField(blank=True, default=0)
    rank = models.ForeignKey('Rank', on_delete=models.SET_DEFAULT, default=4)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default-user.png')

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

       
    def __str__(self):
        return self.username


class Rank(models.Model):
    CHOICES = (
        ('Platinum', 'P'),
        ('Gold', 'G'),
        ('Silver', 'S'),
        ('Bronze', 'B'),
        ('Amateur', 'A')
    )
    title = models.CharField(choices=CHOICES, max_length=10)
    image = models.ImageField(upload_to="ranks/",null=True, blank=True)

    def __str__(self):
        return self.title


class Player(models.Model):
    CHOICES = (
        ('X', 'X'),
        ('O', 'O')
    )
    nickname = models.CharField(max_length=100, unique=True)
    # code = models.CharField(max_length=100, unique=True, default='')
    image = models.CharField(max_length=120, blank=True, null=True)
    choice = models.CharField(choices=CHOICES, max_length=1, default='X')

    def __str__(self):
        return self.nickname


class Game(models.Model):
    name = models.CharField(max_length=30, unique=True)
    player = models.ManyToManyField(Player, related_name='player', blank=True)

    def __str__(self):
        return self.name
