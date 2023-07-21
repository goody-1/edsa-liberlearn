from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from liberlearn.accounts.models import User

from .fields import OrderField

DEFAULT_MENTOR_ID = 2


class Subject(models.Model):
    """The Subject Table, has one or more courses"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Course(models.Model):
    """Course Table, related to an mentor and a Subject"""

    mentor = models.ForeignKey(
        User,
        related_name="courses_assigned",
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_MENTOR_ID,
    )
    subject = models.ForeignKey(
        Subject, related_name="courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Module(models.Model):
    """Contains teaching content"""

    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    def __str__(self):
        return f"{self.order}. {self.title}"

    class Meta:
        ordering = ["order"]


class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model_in": ("text", "video", "image", "file"),
            "is_staff": True,
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]


class ItemBase(models.Model):
    mentor = models.ForeignKey(
        User,
        related_name="%(class)s_related",
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_MENTOR_ID,
    )
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    url = models.URLField()


class CareerPath(models.Model):
    pass


class Assessment(models.Model):
    pass


class Comment(models.Model):
    pass


class Review(models.Model):
    pass