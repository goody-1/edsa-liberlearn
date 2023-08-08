from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string

from liberlearn.accounts.models import User

from .fields import OrderField

DEFAULT_MENTOR_ID = 2


class Subject(models.Model):
    """The Subject Table, has one or more courses"""

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    info = models.TextField(default="Subject Information Should Be Here")
    image_link = models.CharField(
        max_length=200, default="https://i.imgur.com/Z5DoxmH.png"
    )
    intro_video = models.CharField(
        max_length=400, default="https://www.youtube.com/embed/9nkR2LLPiYo"
    )

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
    students = models.ManyToManyField(
        User, related_name="courses_joined", blank=True
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


class Lesson(models.Model):
    """Contains teaching content"""

    course = models.ForeignKey(
        Course, related_name="lessons", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    def __str__(self):
        return f"{self.order}. {self.title}"

    class Meta:
        ordering = ["order"]


class Content(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name="contents", on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model_in": ("text", "video", "image", "file"),
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["lesson"])

    def __str__(self):
        return f"{self.content_type}"

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

    def render(self):
        return render_to_string(
            f"course/content/{self._meta.model_name}.html", {"item": self}
        )


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.CharField(max_length=200)


class Image(ItemBase):
    file = models.CharField(max_length=200)


class Video(ItemBase):
    url = models.CharField(max_length=200)


class Assessment(models.Model):
    course = models.ForeignKey(
        Course, related_name="assessments", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200, editable=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"{self.course.title} Assessment"
        super().save(*args, **kwargs)


class Question(models.Model):
    assessment = models.ForeignKey(
        Assessment, related_name="questions", on_delete=models.CASCADE
    )
    text = models.TextField()

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
