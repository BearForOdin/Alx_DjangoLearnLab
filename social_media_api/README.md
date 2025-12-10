# Social Media API — Alx_DjangoLearnLab

## Overview
This Django project implements a simple social media user model and authentication using Django REST Framework token authentication. It includes endpoints for registration, login, and profile management. The user model (`CustomUser`) extends Django's `AbstractUser` and includes `bio`, `profile_picture`, and a self-referential `followers` field.

## Setup
1. Clone repo and navigate into `social_media_api`.
2. Create & activate a virtualenv.
3. `pip install -r requirements.txt` (or `pip install django djangorestframework djangorestframework-authtoken`)
4. Ensure `AUTH_USER_MODEL = 'accounts.CustomUser'` is present in `settings.py`.
5. `python manage.py makemigrations`
6. `python manage.py migrate`
7. `python manage.py createsuperuser` (optional)
8. `python manage.py runserver`

## Endpoints
- `POST /api/accounts/register/` — register new user (returns token)
- `POST /api/accounts/login/` — login (returns token)
- `GET|PUT /api/accounts/profile/` — get/update authenticated user profile

## Notes
- Keep `AUTH_USER_MODEL` set before the first migrations.
- For production storage of media and static files, configure S3 or another storage backend.
- Consider switching to JWT (djangorestframework-simplejwt) for stateless tokens and refresh tokens if needed.