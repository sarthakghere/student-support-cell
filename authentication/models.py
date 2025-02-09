from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group, Permission
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"
        STUDENT = "student", "Student"

    full_name = models.CharField(max_length=255)
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    username = None
    role = models.CharField(
        max_length=7,
        choices=RoleChoices.choices,
        default=RoleChoices.STUDENT,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Unique related name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Unique related name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
