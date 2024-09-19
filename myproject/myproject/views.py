# home/views.py
from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()  # Получаем все посты
    return render(request, 'home.html', {'posts': posts})