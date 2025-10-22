from django.test import TestCase
from .models import CustomUser, CustomerUserManager
from django.contrib import admin
from .admin import CustomUserAdmin

# ======== test_models =======
class CustomUserTests(TestCase):
    """Test cases for the CustomUser model.

    Description:
        Test suite for validating the behavior of the CustomUser model, including user creation, 
        superuser creation, and validation logic.

    Steps performed:
        - Create a user object with an email address and password and verify that creation works correctly.
        - Create a superuser object and verify that the is_staff and is_superuser flags are automatically set.
        - Attempt to create a user object without an email address and verify that a ValueError is raised.
        - Verify that the string representation of a user returns the email address.        
        
    Notes:
        The tests use Django's built-in `TestCase`, which creates a temporary
        database for each test run. This ensures that tests do not affect
        real project data.    
    """
    def test_create_user(self):
        """User creation verification.
    
        Target: creating a user with an email address and password should work.
        """
        user = CustomUser.objects.create_user(email='basic_user@example.com', password='pwd123')
        self.assertEqual(user.email, 'basic_user@example.com')
        self.assertTrue(user.check_password('pwd123'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        
    def test_create_superuser(self):
        """Superuser creation verification.
    
        Target: creating a superuser should automatically set the is_staff and is_superuser flags.
        """
        super_user = CustomUser.objects.create_superuser(email='admin@example.com', password='pwd123')
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)
        
    def  test_create_user_email_required(self):
        """Email validation.
    
        Target: when creating a user without an email address, an exception should be thrown.
        """
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='testpass123')
        
    def test_str_representation(self):
        """String representation check."""
        user = CustomUser.objects.create_user(email='for_str@example.com', password='pwd123')
        self.assertEqual(str(user), 'for_str@example.com')
        

class CustomerUserManagerTests(TestCase):
    """Test cases for the CustomerUserManager model.

    Description:
        Test cases for the CustomUserManager class.

    Steps performed:
        - Create a user object with unnormalized email address and verify that it was normalized.

    Notes:
        The tests use Django's built-in `TestCase`, which creates a temporary
        database for each test run. This ensures that tests do not affect
        real project data.   
    
    """
    def test_create_user_email_normalized(self):
        """Email normalisation check."""
        user = CustomUser.objects.create_user(email='TEST@EXAMPLE.COM', password='pwd123')
        self.assertEqual(user.email, 'TEST@example.com')
        
# ======== test_admin =======
class CustomUserAdminTest(TestCase):
    """Test case for verifying that the CustomUser model is registered in the Django admin site 
       and that the registered ModelAdmin instance for CustomUser is of type CustomUserAdmin.

    Steps:
        1. Import the CustomUser model and the global admin site object.
        2. Use `assertIn()` to verify that CustomUser is registered in `admin.site._registry`.
        3. Use `assertIsInstance()` to ensure the registered instance is of type CustomUserAdmin.

    Notes:
        - This test does not interact with the database directly.
        - It only verifies that admin.py includes a line such as:
              admin.site.register(CustomUser)
        - The _registry attribute is a dictionary where keys are model classes
          and values are their corresponding ModelAdmin instances.

    References:
        - Django Admin site API:
          https://docs.djangoproject.com/en/stable/ref/contrib/admin/
        - admin.site.register():
          https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.site.register
        - assertIn():
          https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertIn
    """
    def test_user_registration(self):
        """Checking model registration in the admin panel."""
        self.assertIn(CustomUser, admin.site._registry)
        self.assertIsInstance(admin.site._registry[CustomUser], CustomUserAdmin)
        
# ======== CRUD_test =======
class UserCRUDTests(TestCase):
    """Test cases for basic CRUD operations on the CustomUser model.

    This class demonstrates how to perform Create, Read, Update, and Delete (CRUD) 
    operations on the `CustomUser` model using Django's ORM in a testing environment. 
    It verifies that user instances can be created, modified, queried, and deleted correctly. 

    Notes on CRUD in this test:
        - Create: `create_user` method of `CustomUserManager`.
        - Read: `get` and `filter` methods of `QuerySet`.
        - Update: Modifying an attribute and calling `.save()` on the model instance.
        - Delete: Calling `.delete()` on the model instance.

    Important observations:
        - Although CRUD usually includes "Index/List" as a common Read operation (R in RIDA), 
          here we use `filter` and `get` instead of a dedicated "list all users" query.
        - `filter(email='...')` returns a QuerySet (which can contain multiple objects).
        - `.exists()` is used to check presence of a record efficiently without loading all fields.
        - `get(email='...')` is used to retrieve exactly one object for validation after update.
        - This demonstrates practical distinctions between filtering/existence checks and retrieving objects.
    
    Behavior summary:
        - Create a new user and verify it exists in the database.
        - Update a field (first_name) and verify that the change is persisted.
        - Delete the user and verify that it no longer exists.

    Testing environment:
        - Inherits from `django.test.TestCase`, which sets up a temporary in-memory database 
          for each test method. Changes do not affect the real database.
        - Each test is isolated: the database is rolled back after the test finishes.

    References:
        - Django ORM QuerySet API: 
            https://docs.djangoproject.com/en/stable/ref/models/querysets/
        - Django Testing framework:
            https://docs.djangoproject.com/en/stable/topics/testing/overview/
    """
    def test_create_update_delete_user(self):
        """Verify Create, Update, and Delete operations on CustomUser.

        Steps:
            1. Create a new user:
                - Use `CustomUser.objects.create_user()` to create a user with a given email and password.
                - Check if the user exists using `filter(...).exists()`.
                  `filter` returns a QuerySet; `.exists()` checks if the QuerySet contains any objects.
                  This is efficient because it does not load the entire object(s) from the database.
            
            2. Update the user:
                - Change the `first_name` attribute.
                - Call `.save()` on the instance to persist the change.
                - Retrieve the user using `get(email='...')` to verify the update.
                  `get` raises an exception if no user or multiple users exist with the given email.
                  This is used here to ensure exactly one object matches the criteria.
            
            3. Delete the user:
                - Call `.delete()` on the user instance.
                - Check using `filter(...).exists()` to ensure the user no longer exists.
                  `exists()` returns `False` when the QuerySet is empty.

        Notes on CRUD vs RIDA:
            - Here "R" (Read) is represented by both `filter(...).exists()` and `get(...)`.
            - "I" (Index/List) is not explicitly implemented because we are not retrieving multiple users 
              for listing; the focus is on one specific object.
            - "D" (Delete) is performed via the `.delete()` method.
            - Using `filter(...).exists()` is different from `get(...)`:
                • `.exists()` only checks **presence** (True/False) without loading the full object.
                • `.get()` loads the actual object to verify its attributes.
            
        Method origins:
            - `CustomUser.objects.create_user()` → from `CustomUserManager.create_user()`.
            - `.filter()` and `.get()` → Django ORM `QuerySet` methods.
            - `.exists()` → Django ORM `QuerySet` method for efficient existence checks.
            - `.save()` and `.delete()` → methods from `django.db.models.Model`.
        """
        user = CustomUser.objects.create_user(email='crud@example.com', password='pwd123')
        self.assertTrue(CustomUser.objects.filter(email='crud@example.com').exists())
        
        user.first_name = 'John'
        user.save()
        self.assertEqual(CustomUser.objects.get(email='crud@example.com').first_name, 'John')
        
        user.delete()
        self.assertFalse(CustomUser.objects.filter(email='crud@example.com').exists())
        