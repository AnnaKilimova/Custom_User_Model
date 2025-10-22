# 🎓 Django Custom User Model
A lightweight Django project demonstrating two approaches to creating custom user models:

- **users_basic** - Represents an application-specific user extending Django’s built-in AbstractUser.
  *This app shows the recommended lightweight approach to user customization - adding optional profile-related fields (e.g., birth_date, title) while preserving all built-in authentication, permission, and admin functionality.*
- **user_advanced** - Implements a fully customized user model using AbstractBaseUser and PermissionsMixin, where authentication is based on the email address instead of a username.
  *This app demonstrates the advanced approach to building a user model, providing full control over authentication fields, custom user manager methods (create_user, create_superuser), and permission behavior.*


## ⚙️ Installation and Environment Setup
### 1. Clone the repository
```bash
git clone git@github.com:AnnaKilimova/python_testing_portfolio.git
```
### 2. Navigate to the project folder:
```bash
cd custom_user_model
```
### 3. Create and activate a virtual environment
#### For MacOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate    
```  
#### For Windows:
```bash
venv\Scripts\activate    
```
### 4. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt    
```
This installs all required packages listed in requirements.txt, ensuring your environment matches the project dependencies.
## 🧩 Task Description
A new application must be created, and a custom User model must be implemented within it.
### 📝 Requirements:
1. Either AbstractUser or AbstractBaseUser in combination with PermissionsMixin may be employed.
2. The selection and number of fields are to be determined at the developer’s discretion.
### 🧪 Running Tests for user_advanced app
```bash
python manage.py test
```
Tests cover:
- User creation
- Superuser creation
- Email validation and normalization
- String representation
- Admin model registration
- Full CRUD operations (Create, Update, Delete)
### 🚀 Running the Application
After tests pass, start the server:
```bash
python manage.py runserver
```
The project will be available at:
```bash
👉 http://127.0.0.1:8000/
```
Available route:
- [/admin/](http://127.0.0.1:8000/admin/) - admin panel

Stop the server:
```bash
^C
```
### **⚠ Attention:** Switching to the users_basic App.
Before switching apps, remove the database and migration files:
```bash
rm db.sqlite3
rm user_advanced/migrations/0*
```
1. Open the file /custom_user_model/custom_user_model/settings.py
- In INSTALLED_APPS, uncomment "users_basic.apps.UsersBasicConfig"
and comment out "user_advanced.apps.UserAdvancedConfig".
- Uncomment AUTH_USER_MODEL = "users_basic.CustomUserBasic"
and comment out the "user_advanced" version.
- Save the file.
2. In the user_advanced app, rename the file tests.py → disabled_tests.py. 
3. In the users_basic app, rename disabled_tests.py → tests.py and uncomment code in this file.
4. Create and apply new migrations for users_basic:
```bash
python manage.py makemigrations users_basic
python manage.py migrate
```
### 🧪 Running Tests for users_basic App
```bash
python manage.py test
```
Tests cover:
- Verifying that birth_date and title fields are saved correctly
- Display behavior when the title field is filled or empty
- Correct string representation depending on which fields are provided
- Registration of CustomUserBasic in Django Admin
- Presence of birth_date and title fields in the admin fieldsets

### 🙋‍♂️ Create superuser
```bash
python manage.py createsuperuser
```

### 🚀 Running the Application
After tests pass, start the server:
```bash
python manage.py runserver
```
The project will be available at:
```bash
👉 http://127.0.0.1:8000/
```
Available route:
- [/admin/](http://127.0.0.1:8000/admin/) - admin panel
## 🧱 Project Structure
```
custom_user_model/
│
├── custom_user_model/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── user_advanced/
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
│
├── users_basic/
│   ├── models.py
│   ├── views.py
│   ├── apps.py
│   ├── disabled_tests.py
│   └── migrations/
│       └── __init__.py
│
└── manage.py
```

