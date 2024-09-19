from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField('Заголовок записи', max_length=200)
    description = models.TextField()
    author = models.CharField('Имя Автора', max_length=200)
    date = models.DateField('Дата Публикации')
    createdat = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f'{self.title}, {self.author}' 
    
    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Запись'


    




    