# Note that we're importing models from `djongo`
from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name,password2, password):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')
        if not first_name:
            raise ValueError('First Name is required')
        if not last_name:
            raise ValueError('Last Name is required')
        if not password:
            raise ValueError('Password is required')
        if not password2:
            raise ValueError('Password 2 is required')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, user_type, password):
        user = self.create_user(
            # email=self.normalize_email(email),
            password=password,
            username=username,
            user_type=user_type,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # id = models.CharField(max_length=24,null=False, blank=False, primary_key=True)
    username = models.CharField(
        verbose_name="username", max_length=60, null=False, blank=False, unique=False)
    first_name = models.CharField(
        verbose_name="first_name", max_length=60, null=False, blank=False, unique=False)
    last_name = models.CharField(
        verbose_name="last_name", max_length=60, null=False, blank=False, unique=False)
    email = models.EmailField(
        verbose_name="email", null=False, blank=False, unique=True)
    created_at = models.DateTimeField(
        verbose_name='created_at', auto_now_add=True)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # password = models.CharField(null=False, blank=False)

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['user_type']


    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    class Meta:
        app_label = 'user'
        db_table = 'users'
