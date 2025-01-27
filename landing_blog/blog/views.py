from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import CommentForm, RegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q

def landing_page(request):
    posts = Post.objects.order_by('-created_at')[:3]
    return render(request, 'blog/landing_page.html', {'posts': posts})

def blog_list(request):
    posts = Post.objects.order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'posts': posts})

def blog_detail(request, author_username, slug):
    post = Post.objects.get(author__username=author_username, slug=slug)
    comments = post.comments.filter(parent__isnull=True).order_by('-created_at')
    comment_form = CommentForm()
    similar_posts = Post.objects.all().exclude(id=post.id).order_by('-created_at')[:5]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_id = request.POST.get('parent_id')
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)

            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user if request.user.is_authenticated else None
            new_comment.parent = parent_comment
            new_comment.save()
            return HttpResponseRedirect(reverse('blog_detail', kwargs={'author_username': author_username, 'slug': slug}) + '#comments')

    return render(request, 'blog/blog_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct().order_by('-created_at')
    else:
        posts = Post.objects.none()
    return render(request, 'blog/blog_list.html', {'posts': posts, 'search_query': query})

def delete_comment(request, comment_id):
    if request.user.is_superuser: # Check for superuser status
        comment = Comment.objects.get(pk=comment_id)
        post_slug = comment.post.slug
        author_username = comment.post.author.username
        comment.delete()
        return redirect('blog_detail', author_username=author_username, slug=post_slug)
    else:
        return redirect('blog_list') # Redirect to blog list if not admin
