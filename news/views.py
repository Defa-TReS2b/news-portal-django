from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, SubscribersCategory
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm, SubscribeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'posts.html'
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

class SearchList(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'search.html'
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.state = 13
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'create.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')

class SubscriberView(LoginRequiredMixin, CreateView):
    model = SubscribersCategory
    form_class = SubscribeForm
    template_name = 'subscribe.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        subscribe = form.save(commit=False)
        subscribe.subscriber = User.objects.get(pk=self.request.user.id)
        return super(SubscriberView, self).form_valid(form)