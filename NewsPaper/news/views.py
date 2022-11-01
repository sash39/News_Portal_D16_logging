from django.urls import reverse_lazy
from django.shortcuts import render
from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = '-posting_time'
    template_name = 'posts.html'
    context_object_name = 'posts'


    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = "Новые статьи в пятницу"
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        con = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        con['filterset'] = self.filterset
        return con


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
