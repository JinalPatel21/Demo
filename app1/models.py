from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, **extra_fields):
        """Creates and saves a User with the given email"""
        if not email:
            raise ValueError(_('The email must be set'))

        password = extra_fields.get('password', None)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            **kwargs
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name=_('email address'), unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    first_name = models.CharField(null=True, blank=True)
    last_name = models.CharField(null=True, blank=True)
    is_verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name="Date Joined", default=timezone.now)
    last_active = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(verbose_name="Last Login", auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '{} - {}'.format(self.pk, self.email)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class Category(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

ARTICLE_TYPES = [
    ("UN", "Unspecified"),
    ("TU", "Tutorial"),
    ("RS", "Research"),
    ("RW", "Review"),
]

class Article(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=ARTICLE_TYPES, default="UN")
    categories = models.ForeignKey(Category, blank=True,null=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}: {self.title} ({self.created_datetime.date()})"

    def type_to_string(self):
        return dict(ARTICLE_TYPES).get(self.type, "Unspecified")
