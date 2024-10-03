
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render
from .models import Post, Category
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


def search_view(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query)
        )
    else:
        posts = Post.objects.none()

    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'search_results.html', context)

class PostByCategoryView(ListView):
    model = Post
    template_name = 'category_posts.html'  # Шаблон для отображения постов по категориям
    context_object_name = 'posts'

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        return Post.objects.filter(category__name__iexact=category_name) 

def autocomplete_search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query)
        ).select_related('category')[:10]  # Ограничиваем до 10 результатов
        results = []
        for post in posts:
            results.append({
                'id': post.id,
                'title': post.title,
                'category': post.category.name
            })
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})


class CategoryPostListView(ListView):
    model = Post
    template_name = 'category_posts.html'  # Укажите шаблон для отображения постов
    context_object_name = 'posts'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')  # Получаем id категории из URL
        return Post.objects.filter(category_id=category_id)  # Фильтруем посты по категории

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(id=self.kwargs.get('category_id'))  # Добавляем категорию в контекст
        return context

def home(request):
    posts = Post.objects.all()  # Получаем все посты
    return render(request, 'home.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'home.html'  
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 12
   


def home_view(request):
    posts = Post.objects.all()  # Получение всех постов
    return render(request, 'home.html', {'posts': posts})

class UserPostListView(ListView):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date')    


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'date', 'author', 'description', 'category']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Загружаем все категории
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
     

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'about.html', {'title': 'О клубе Python Bites'})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа после регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html') 