from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserBasic(AbstractUser):
    """Represents an application-specific user, extending Django's built-in AbstractUser.

    This model extends the default Django user by adding optional profile-related fields,
    while preserving all built-in authentication, permissions, and admin functionality.
    It demonstrates the recommended approach for lightweight user customization.

    Inheritance:
        Inherits from:
            - django.contrib.auth.models.AbstractUser
              → which itself inherits from AbstractBaseUser and PermissionsMixin.

        AbstractUser already includes:
            - Core authentication fields and methods (password handling, last_login)
              from AbstractBaseUser.
            - Permission and group management (is_superuser, groups, user_permissions)
              from PermissionsMixin.
            - Common user identity fields:
                • username (unique identifier)
                • first_name
                • last_name
                • email
                • is_staff
                • is_active
                • date_joined
            - Default manager: UserManager (provides create_user / create_superuser methods)

    Table name:
        `users_customuserbasic` (generated automatically by Django as <app_label>_<model_name>)

    Attributes:
        id (int):
            Auto-incrementing primary key (automatically created by Django).

        username (str):
            Unique username used for login and identification (inherited from AbstractUser).

        first_name (str):
            Optional first name field (inherited).

        last_name (str):
            Optional last name field (inherited).

        email (str):
            Optional email address field (inherited). Not unique by default in AbstractUser.

        birth_date (datetime.date | None):
            Optional date of birth field. May be used for age verification or user profiling.
            - `null=True`: allows storing NULL in the database.
            - `blank=True`: allows leaving the field empty in Django forms.

        title (str | None):
            Optional honorific or short descriptive title (e.g., “Dr.”, “Mr.”, “Team Lead”).
            - `max_length=50`: stored as a short VARCHAR.
            - `blank=True`: optional field in forms.

        password (str):
            Hashed password field (inherited from AbstractBaseUser). Never stores plaintext.

        is_staff (bool):
            Indicates whether the user can log in to the admin site (inherited).

        is_active (bool):
            Marks whether the user account is currently active (inherited).

        is_superuser (bool):
            Grants all permissions without explicitly assigning them (from PermissionsMixin).

        date_joined (datetime):
            Date/time when the user account was created (inherited).

        groups (ManyToMany[Group]):
            Relationship for role-based permissions (from PermissionsMixin).

        user_permissions (ManyToMany[Permission]):
            Relationship for fine-grained permission management (from PermissionsMixin).

    Relationships:
        - No custom relationships added.
        - Inherits Many-to-Many relationships to auth.Group and auth.Permission
          via PermissionsMixin.

    Methods:
        get_full_name() -> str:
            Inherited method returning "<first_name> <last_name>".
        
        get_short_name() -> str:
            Inherited method returning first_name.

        get_full_title_name() -> str:
            Custom convenience method returning a formatted display name that includes
            `title` if provided (e.g., “Dr. Alice Smith”).
        
        Example:
            user = CustomUserBasic(first_name="Alice", last_name="Smith", title="Dr.")
            user.get_full_title_name()
            'Dr. Alice Smith'

    Admin Integration:
        - Fully compatible with Django's default UserAdmin.
        - To show `birth_date` and `title` fields in the Django admin, subclass `UserAdmin`
          and extend `fieldsets` and `add_fieldsets`.

        Example (admin.py):
            from django.contrib import admin
            from django.contrib.auth.admin import UserAdmin
            from .models import CustomUserBasic

            @admin.register(CustomUserBasic)
            class CustomUserBasicAdmin(UserAdmin):
                fieldsets = UserAdmin.fieldsets + (
                    ('Additional Info', {'fields': ('birth_date', 'title')}),
                )
                add_fieldsets = UserAdmin.add_fieldsets + (
                    ('Additional Info', {'fields': ('birth_date', 'title')}),
                )

    Notes:
        - This model is intended for applications where the default username-based
          authentication is acceptable.
        - To switch to email-based login or other custom identifiers, use
          AbstractBaseUser + PermissionsMixin instead.
        - Must be referenced in Django settings before running the first migration:
            AUTH_USER_MODEL = 'users.CustomUserBasic'
        - All other apps should reference this model using:
            settings.AUTH_USER_MODEL
          instead of hardcoding 'auth.User'.

    References:
        - Django Documentation: 
            https://docs.djangoproject.com/en/stable/topics/auth/customizing/
            https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.AbstractUser
    """
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of birth')
    title = models.CharField(max_length=50, blank=True, verbose_name='Title')


    def get_full_title_name(self) -> str:
        """Return a full name prefixed by title if available.

        Example:
            >>> user = CustomUserBasic(first_name='Alice', last_name='Smith', title='Dr.')
            >>> user.get_full_title_name()
            'Dr. Alice Smith'
        """
        full = self.get_full_name().strip()
        if self.title:
            return f"{self.title} {full}".strip()
        return full