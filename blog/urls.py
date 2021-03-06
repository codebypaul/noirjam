from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

urlpatterns = [
    # path("", views.home, name="blog_home"),
    path("", PostListView.as_view(), name="actually_blog"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/new", PostCreateView.as_view(), name="post-create"),
    path("about/", views.about, name="blog_about"),
]