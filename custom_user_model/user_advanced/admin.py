from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """"Admin configuration class for managing CustomUser instances in Django Admin.

    This class defines how the CustomUser model is displayed, edited, and managed
    within the Django administration interface. It extends Django's built-in
    `UserAdmin` class, which provides advanced functionality for handling user
    models, including password management, permissions, and group assignments.

    Inheritance:
        Inherits from:
            - django.contrib.auth.admin.UserAdmin

        The base `UserAdmin` class provides:
            • Preconfigured views for listing, adding, and editing users.  
            • Password hashing and validation support.  
            • Integration with Django's permission and group system.  

    Purpose:
        When using a custom user model (especially one based on AbstractBaseUser),
        Django's default `UserAdmin` cannot automatically determine which fields
        to display or edit.  
        This class customizes the admin interface for the `CustomUser` model by:
            • Replacing the default `username` field with `email`.
            • Organizing fields into clear logical sections.
            • Controlling which fields appear when adding or editing users.
            
    Attributes:            
        list_display (tuple[str]):
            Specifies which model fields are displayed in the user list view
            (the table view in Django Admin under “Users”).

            Each element can be:
                • A field name on the model.
                • A method defined in the admin class that returns a value.
                • A callable on the model (e.g., a property).

            Purpose:
                Provides a quick overview of key user information directly in
                the admin list — without opening each record individually.

        list_filter (tuple[str]):
            Adds filtering options in the right sidebar of the admin interface.

            Purpose:
                Allows administrators to quickly filter users by activity status,
                admin rights, or group membership.  
                Filters make it easier to manage large user datasets.

        ordering (tuple[str]):
            Defines the default ordering of records in the list view.

            Purpose:
                Determines how users are sorted when displayed in the admin table.
                Sorting by `email` is logical in email-based authentication systems.

        search_fields (tuple[str]):
            Specifies which fields are searchable through the search bar
            located above the user list in the admin interface.

            Purpose:
                Allows administrators to search users by email or name.
                The search uses case-insensitive partial matching by default.
    
        Fieldsets:
            Defines how fields are grouped and displayed on the form.

            fieldsets = (
                (None, {'fields': ('email', 'password')}),
                    → Basic authentication information.
                ('Personal information', {'fields': ('first_name', 'last_name', birth_date)}),
                    → Optional user identity details.
                ('Rights', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                    → User permissions, admin access, and role assignments.
                ('Dates', {'fields': ('date_joined', 'last_login')}),
                    → Account activity tracking and registration date.
            )

            Each tuple contains:
                1. A section title (str or None)
                2. A dictionary with configuration options (fields, classes, etc.)

            These sections organize the form layout in the Django Admin panel,
            improving readability and usability for administrators.

        Add Fieldsets:
            Defines the layout for the form in the admin.

            Key points:
                • `'classes': ('wide',)` applies a CSS class for a more spacious layout.
                • `'fields'` includes both password inputs (password1 & password2)
                for validation and confirmation.
                • Includes essential flags for user activation and access level.

    Registration:
        The decorator `@admin.register(CustomUser)` automatically registers
        this admin configuration with the Django admin site, linking the
        `CustomUser` model and `CustomUserAdmin` class.  
        This eliminates the need to call `admin.site.register(CustomUser, CustomUserAdmin)` manually.

    Behavior Summary:
        • Users are authenticated via email (not username).  
        • Passwords are securely hashed and managed through `UserAdmin`.  
        • Staff can assign permissions and group memberships.  
        • The admin interface cleanly separates personal, permission, and
          activity information for each user.

    References:
        - Django Documentation:
            https://docs.djangoproject.com/en/stable/ref/contrib/admin/
            https://docs.djangoproject.com/en/stable/topics/auth/customizing/#a-full-example
            https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.admin.UserAdmin
    """
    list_display = ('email', 'first_name', 'last_name', 'birth_date', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name', 'birth_date')    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'last_name', 'birth_date')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )

