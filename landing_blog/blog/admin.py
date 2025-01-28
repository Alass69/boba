from django.contrib import admin
from .models import Post
from .forms import PostAdminForm

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'created_at')
    filter_horizontal = ('tags',)

admin.site.register(Post, PostAdmin)
