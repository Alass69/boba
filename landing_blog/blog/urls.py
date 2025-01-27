from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<str:author_username>/<str:slug>/', views.blog_detail, name='blog_detail'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('register/', views.register, name='register'),
    path('search/', views.search_posts, name='search_posts'),
]
