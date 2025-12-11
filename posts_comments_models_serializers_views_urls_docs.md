# Posts & Comments — Implementation Guide

This document contains the full code and instructions to add a `posts` app to your `social_media_api` Django project. It includes models, serializers, viewsets, permissions, routing (DRF routers), pagination, filtering, testing notes, and Postman examples.

---

## Quick shell commands

```bash
# from project root
python manage.py startapp posts
# add 'posts' to INSTALLED_APPS in settings.py

# create migrations and migrate
python manage.py makemigrations posts
python manage.py migrate
```

---

## 1) posts/models.py

```python
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post_id}"
```

Notes:
- `related_name` makes reverse relations (`user.posts`, `post.comments`) easy.

---

## 2) posts/serializers.py

```python
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username', 'title', 'content',
            'created_at', 'updated_at', 'comments', 'comments_count'
        ]
        read_only_fields = ['id', 'author', 'author_username', 'created_at', 'updated_at', 'comments', 'comments_count']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)
```

Notes:
- `create()` methods set `author` from the request user so clients don't submit it.
- `comments` is nested read-only for convenience.

---

## 3) posts/permissions.py

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow owners of an object to edit/delete it; others read-only."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the object's author
        return getattr(obj, 'author', None) == request.user
```

---

## 4) posts/views.py

```python
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        # optional filtering by post id via query param ?post=1
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post')
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset
```

Notes:
- `SearchFilter` allows `?search=keyword` to search title/content.
- Comments can be filtered by `?post=<id>`.

---

## 5) posts/urls.py

```python
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
```

Include these in project urls.py, for example:

```python
# social_media_api/urls.py
path('api/', include('posts.urls')),
```

This will expose endpoints like:
- `GET /api/posts/` (list)
- `POST /api/posts/` (create)
- `GET /api/posts/<id>/` (retrieve)
- `PUT/PATCH /api/posts/<id>/` (update)
- `DELETE /api/posts/<id>/` (delete)

And similarly for `/api/comments/`.

---

## 6) Pagination & Filtering

- Pagination is implemented with `StandardResultsSetPagination` and default `page_size=10`.
- Filtering/search via DRF `SearchFilter` (`?search=term`) and `OrderingFilter` (`?ordering=created_at`).
- Additional filters (e.g., by author) can be added using `django-filter` if needed.

To enable `django-filter` add to `INSTALLED_APPS` and update `REST_FRAMEWORK` with `DjangoFilterBackend`.

---

## 7) Tests (basic examples)

`posts/tests.py` (examples):

```python
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bob', password='pass')
        self.client.login(username='bob', password='pass')

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'Hello', 'content': 'World'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)
```

---

## 8) Postman / curl examples

Create a post:

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"Hello world"}'
```

List posts with search:

```
GET /api/posts/?search=Hello
```

List comments for a post:

```
GET /api/comments/?post=1
```

---

## 9) Documentation notes to add to README

- Briefly document endpoints, required auth (Token), example requests (see Postman examples), and note pagination.
- Mention ability to search posts with `?search=` and to order with `?ordering=`.

---

## 10) Next steps / optional enhancements

- Add `like` model or `ManyToMany` field for likes.
- Add signals to notify post authors of new comments.
- Use `django-filter` for advanced filtering (by author, date range, etc.).
- Add throttling or rate-limits.
- Add serializers for `create`/`update` that validate content length.

---

*End of "Posts & Comments" implementation guide.*

