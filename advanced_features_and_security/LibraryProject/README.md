# Django Permissions and Groups Setup

## Models
- `Article` model has custom permissions:
  - `can_view`
  - `can_create`
  - `can_edit`
  - `can_delete`

## Groups
- **Editors**: Can create and edit articles.
- **Viewers**: Can view articles.
- **Admins**: Can view, create, edit, and delete articles.

## Usage
- Assign users to groups via Django admin.
- Permissions are enforced in views using `@permission_required`.

Example:
```python
@permission_required('advanced_features_and_security.can_edit', raise_exception=True)
def article_edit(request, pk):
    ...
