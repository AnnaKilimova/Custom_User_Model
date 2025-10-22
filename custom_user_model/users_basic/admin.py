from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUserBasic
 
@admin.register(CustomUserBasic)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for managing CustomUserBasic instances in Django Admin.

    This class customizes how CustomUserBasic is displayed, edited, and managed
    within the Django admin interface. It extends Django's built-in UserAdmin,
    which provides preconfigured views and behavior for user management.

    Inheritance:
        Inherits from django.contrib.auth.admin.UserAdmin, which provides:
            • Views for listing, adding, and editing users
            • Password hashing and validation
            • Integration with permissions and groups

    Purpose:
        Since CustomUserBasic adds custom fields (birth_date, title) to AbstractUser,
        this admin class ensures:
            • Default username authentication is preserved
            • Admin forms include all relevant fields
            • Custom fields are added under a separate "Additionally" section

    Attributes:
        fieldsets (tuple):
            Grouping of fields in the admin form. Extends the default UserAdmin.fieldsets
            and adds 'birth_date' and 'title' in the "Additionally" section.

    Behavior Summary:
        • Users are authenticated via username
        • Passwords are securely hashed and managed
        • Staff can assign permissions and group memberships
        • Personal, permission, and activity fields are clearly separated
        • Custom fields (birth_date and title) are displayed in their own section

    Registration:
        The @admin.register(CustomUserBasic) decorator registers this admin class
        with the Django admin site automatically.

    References:
        - https://docs.djangoproject.com/en/stable/ref/contrib/admin/
        - https://docs.djangoproject.com/en/stable/topics/auth/customizing/#a-full-example
        - https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.admin.UserAdmin
    """
    fieldsets = UserAdmin.fieldsets + (('Additionally', {'fields': ('birth_date', 'title')}),)
