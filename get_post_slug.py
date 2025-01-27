from blog.models import Post

post = Post.objects.first()
if post:
    print(post.slug)
else:
    print('No posts found.')
