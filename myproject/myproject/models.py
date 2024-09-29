from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)



class MyModel(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField('Заголовок записи', max_length=200)
    description = models.TextField()
    author = models.CharField('Имя Автора', max_length=200)
    date = models.DateField('Дата Публикации')
    createdat = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 

    def __str__(self):

        return f'{self.title}, {self.author}' 
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Запись'


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Изменено
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Изменено
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )



    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    