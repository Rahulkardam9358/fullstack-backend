from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import UserManager as BaseManager


class UserManager(BaseManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name",]
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'

    
    @property
    def fullName(self):
        return f'{self.first_name } {self.last_name}'


class Address(models.Model):
    ADDRESS_TYPE = [
        ('HOME', 'Home'),
        ('OFFICE', 'Office'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=ADDRESS_TYPE, default='Home')
    address_line1 = models.CharField(max_length=1000)
    address_line2 = models.CharField(max_length=1000)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=6)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return f'{self.user.email} | {self.id}'

    class Meta:
        db_table = 'address'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'


