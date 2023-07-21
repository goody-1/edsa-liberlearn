from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email and not username:
            raise ValueError(_("Either Email or Username field must be set"))
        if email:
            self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not email and not username:
            raise ValueError(_("Either Email or Username field must be set"))

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # This sets the hashed password
        user.save(using=self._db)
        return user
        # extra_fields.setdefault("is_admin", True)
        return self._create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Email Address"), unique=True, blank=True, null=True)
    username = models.CharField(
        _("Username"), max_length=30, unique=True, blank=True, null=True
    )
    ROLE_CHOICES = (
        ("student", _("Student")),
        ("mentor", _("Mentor")),
        ("facility", _("Facility")),
    )

    role = models.CharField(_("Role"), max_length=10, choices=ROLE_CHOICES, blank=True)
    first_name = models.CharField(_("First Name"), max_length=30, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=30, blank=True)
    is_active = models.BooleanField(_("Active"), default=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)

    # Computed properties
    @property
    def is_mentor(self):
        return self.role == "mentor"

    @property
    def is_facility(self):
        return self.role == "facility"

    @property
    def is_student(self):
        return self.role == "student"

    # Change this to 'email' if you want email as the default login field
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email"
    ]  # Keep it empty if you don't want any additional required fields for signup

    objects = UserManager()

    def __str__(self):
        return self.username or self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="student"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    batch = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user

    def save(self, *args, **kwargs):
        if not (self.first_name and self.last_name and self.batch and self.roll_no):
            raise ValidationError("All fields in Student model must be filled")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")


class Mentor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="mentor"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        if not (self.first_name and self.last_name and self.subject):
            raise ValidationError("All fields in Mentor model must be filled")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Mentor")
        verbose_name_plural = _("Mentors")


class Facility(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="facility"
    )
    admin_officer_first_name = models.CharField(max_length=100)
    admin_officer_last_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    facility_name = models.CharField(max_length=100)
    facility_full_address = models.TextField()

    def __str__(self) -> str:
        return self.facility_name

    def save(self, *args, **kwargs):
        if not (
            self.admin_officer_first_name
            and self.admin_officer_last_name
            and self.state
            and self.town
            and self.facility_name
            and self.facility_full_address
        ):
            raise ValidationError("All fields in Facility model must be filled")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")
