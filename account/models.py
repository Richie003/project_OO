from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, tel, ip, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            ip=ip,
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, tel, ip, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            ip=ip,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, tel, ip, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            ip=ip,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

#

sub_plan = (
    ('None', ''),
    ("Merchant", "Merchant"),
    ("Customer", "Customer"),
)

#

class User(AbstractBaseUser):
    objects = UserManager()
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    username = models.CharField(default='', verbose_name='username', unique=True, null=True, blank=False,
                                max_length=30)
    tel = models.CharField(default='', null=True, blank=True, max_length=11)
    category = models.CharField(max_length=9, blank=False, default='', choices=sub_plan)
    ip = models.CharField(default='', max_length=200, blank=True)
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    auser = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'tel', 'ip']  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        # concatenate = '%s %s' % (self.first_name, self.last_name)
        return str(self.username)

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_user(self):
        """Is it a user?"""
        return self.auser

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active


class Subscription(models.Model):
    sub_plan = (
        ("Merchant", "Merchant"),
        ("Customer", "Customer"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default='1', null=True, on_delete=models.SET_NULL)
    plan = models.CharField(max_length=9, blank=False, default='', choices=sub_plan)

    def __str__(self):
        concatenate = '%s%s%s' % (self.user, '-', self.plan)
        return str(concatenate)


class Category(models.Model):
    user = models.CharField(max_length=200, default='')
    user_cat = models.CharField(max_length=200, default='')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_cat)


class PaidUser(models.Model):
    CATEGORY = (
        ('Paid', 'Paid'),
        ('Not_Paid', 'Not_Paid'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, default=1, on_delete=models.CASCADE)
    category = models.CharField(max_length=8, default='', choices=CATEGORY)
    created = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()

    def __str__(self):
        return str(self.user)


class Bio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    display_photo = models.ImageField(upload_to='display_photo/', default='profile.png', blank=True)
    description = models.TextField(max_length=200, default='')
    active_user = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.user)

#