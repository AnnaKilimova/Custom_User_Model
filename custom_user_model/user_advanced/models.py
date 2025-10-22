from __future__ import annotations
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from typing import Any


class CustomerUserManager(BaseUserManager):
    """Custom manager class responsible for creating and managing user instances
    of the CustomUser model.

    This manager extends Django's BaseUserManager and defines the standard
    methods for creating both regular users and superusers in a custom user model
    that does not use `username` as its primary identifier (email-based login).
    
    Inheritance:
        Inherits from:
            - django.contrib.auth.models.BaseUserManager

        BaseUserManager provides:
            • Helper methods for email normalization (normalize_email)
            • Database manager interface (create, filter, save, etc.)
            • The recommended pattern for defining create_user() and create_superuser()

        In Django's default UserManager (used by AbstractUser),
        BaseUserManager is also the parent class.
        
    Purpose:
        Django requires every custom user model (based on AbstractBaseUser)
        to define its own manager that knows:
            - how to create users properly (with password hashing),
            - how to create superusers with the correct permission flags,
            - and how to normalize the identifying field (email).

        Without this manager, the commands `createsuperuser` and `User.objects.create_user()`
        would not know how to instantiate and configure user objects.  
        
    Notes:
        - This class follows Django's official recommendation for implementing
          managers for custom user models.
        - Any additional user types (e.g., staff, moderators) can be created by
          extending these methods or by adding custom manager methods.

    References:
        - Django Documentation:
            https://docs.djangoproject.com/en/stable/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
            https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.BaseUserManager 
    """
    
    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> CustomUser:
        """Create and save a regular user with the given email and password.

        Args:
            email (str): The user's email address. Required and must be unique.
            password (str | None): The raw password to be hashed and stored.
            **extra_fields: Additional attributes (e.g., first_name, last_name).

        Raises:
            ValueError: If no email is provided.
            
        Internal Methods Used:
            normalize_email(email):
                Provided by BaseUserManager.
                Converts the domain part of the email to lowercase to ensure consistency:
                    "USER@Example.COM" → "USER@example.com"

            self.model:
                A dynamic reference to the associated user model (CustomUser2 in this case).
                Django automatically assigns this when the manager is attached via:
                    objects = CustomUser2Manager()

            set_password(password):
                Method inherited from AbstractBaseUser.
                Hashes the plaintext password before saving.

        Steps:
            1. Validate that the email field is not empty.
            2. Normalize the email (lowercase the domain part) using
               BaseUserManager.normalize_email().
            3. Instantiate the user model:
               user = self.model(email=email, **extra_fields)
            4. Hash the password using user.set_password(password).
            5. Save the user instance to the database.
            6. Return the newly created user object.
            
        Relationship to CustomUser:
            This manager is attached to CustomUser via:
                objects = CustomUserManager()

            It ensures:
                - Consistent creation of users and superusers.
                - Correct hashing of passwords.
                - Compatibility with Django's authentication commands:
                    - `python manage.py createsuperuser`
                    - `User.objects.create_user()`

            Without this manager, user creation commands would fail
            because AbstractBaseUser does not include a default manager.
        """
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email: str, password: str | None = None, **extra_fields: Any) -> CustomUser:
        """Create and save a superuser with full administrative privileges.
        
        Args:
            email (str): The superuser's email address.
            password (str | None): The raw password to be hashed and stored.
            **extra_fields: Any additional fields for the user.

        Steps:
            1. Set default flags if not explicitly provided:
               extra_fields.setdefault('is_staff', True)
               extra_fields.setdefault('is_superuser', True)
            2. Call create_user() to handle instance creation and password setup.
            3. Return the created superuser instance.

        Important:
            - Both is_staff and is_superuser must be True for Django admin access.
            - These flags are checked by Django's authentication and admin subsystems.            
            
        Field Behavior:
            The manager automatically sets or validates the following flags:
            • is_staff: indicates admin-site access (required for /admin/ login).
            • is_superuser: grants all permissions automatically.

            These values are used internally by Django's permission system and admin checks.            
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Represents a fully customized user model where authentication is based on email.

    This implementation demonstrates the "advanced" approach to creating a custom
    Django user model using AbstractBaseUser + PermissionsMixin, allowing full control
    over authentication fields, behavior, and permissions.

    Inheritance:
        Inherits from:
            - django.contrib.auth.models.AbstractBaseUser
              → provides core authentication functionality:
                • password hashing & verification (set_password, check_password)
                • last_login tracking
                • is_authenticated / is_anonymous properties

            - django.contrib.auth.models.PermissionsMixin
              → adds permission and group management:
                • is_superuser flag
                • groups (ManyToMany[Group])
                • user_permissions (ManyToMany[Permission])
                • has_perm(), has_module_perms() methods

        The model uses a custom manager:
            - CustomUserManager (inherits from BaseUserManager)
              → provides create_user() and create_superuser() methods,
                defining how user instances are created and saved.
                
        Purpose:
            This model replaces Django's default User model (which uses `username`)
            with a completely email-based authentication system.

            It explicitly defines all fields that AbstractUser would normally provide,
            giving developers full control over their configuration, defaults, and behavior.
            
        Attributes:
            email (str):
                Unique email address used as the primary identifier for login.
                - Required: Yes
                - Unique: True
                - Acts as USERNAME_FIELD (used during authentication).

            first_name (str):
                Optional user's first name.
                - max_length=30
                - blank=True (optional in forms)

            last_name (str):
                Optional user's last name.
                - max_length=30
                - blank=True (optional in forms)
                
            birth_date (datetime.date | None):
                Optional date of birth field. May be used for age verification or user profiling.
                - `null=True`: allows storing NULL in the database.
                - `blank=True`: allows leaving the field empty in Django forms.

            is_staff (bool):
                Indicates whether the user can log into the Django admin site.
                - default=False
                - Django admin checks this flag to allow access:
                if user.is_active and user.is_staff → grant access.

            is_active (bool):
                Controls whether the account is considered active.
                - default=True
                - If set to False, Django's authentication system will prevent login.
                - Used by `django.contrib.auth.authenticate()`.

            date_joined (datetime):
                Records when the user account was created.
                - default=django.utils.timezone.now

            password (str):
                Securely hashed password, provided by AbstractBaseUser.
                Never stores plaintext passwords.

            last_login (datetime | None):
                Timestamp of the last successful authentication.
                Inherited from AbstractBaseUser.

            is_superuser (bool):
                Boolean flag granting all permissions automatically.
                Inherited from PermissionsMixin.
                Automatically set to True when using create_superuser().

            groups (ManyToMany[Group]):
                Role-based permission groups.
                Inherited from PermissionsMixin.

            user_permissions (ManyToMany[Permission]):
                Fine-grained permission assignments.
                Inherited from PermissionsMixin.
                
        Special Attributes:
            USERNAME_FIELD = 'email'
                - Tells Django to use `email` as the unique identifier for login.

            REQUIRED_FIELDS = []
                - Defines which fields are required when creating a superuser
                interactively (via createsuperuser command).
                - Here, no extra fields are required beyond email & password.
                
        References:
            Django Documentation:
                - Customizing authentication:
                https://docs.djangoproject.com/en/stable/topics/auth/customizing/
                - AbstractBaseUser:
                https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.AbstractBaseUser
                - PermissionsMixin:
                https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.PermissionsMixin
                - BaseUserManager:
                https://docs.djangoproject.com/en/stable/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model   
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name='Date of birth')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomerUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        """Returns the user's email address for a human-readable representation.

        (Inherited from AbstractBaseUser / PermissionsMixin):
            set_password(raw_password)
            check_password(raw_password)
            get_session_auth_hash()
            has_perm(perm, obj=None)
            has_module_perms(app_label)
        """
        return self.email