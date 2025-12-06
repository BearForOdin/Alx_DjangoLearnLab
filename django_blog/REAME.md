Blog Post CRUD
--------------
URLs:
- List:     /posts/                (PostListView)
- Create:   /posts/new/            (PostCreateView) - login required
- Detail:   /posts/<int:pk>/       (PostDetailView)
- Edit:     /posts/<int:pk>/edit/  (PostUpdateView) - author only
- Delete:   /posts/<int:pk>/delete/(PostDeleteView) - author only

Permissions:
- Create: logged-in users only
- Edit/Delete: only the post's author

Forms:
- PostForm (ModelForm) supplies 'title' and 'content'

Templates:
- blog/posts/post_list.html
- blog/posts/post_detail.html
- blog/posts/post_form.html
- blog/posts/post_confirm_delete.html
