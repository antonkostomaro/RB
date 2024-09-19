# home/views.py
from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all().order_by('-created_at')  # Получаем все посты, отсортированные по дате
    return render(request, 'home/home.html', {'posts': posts})
