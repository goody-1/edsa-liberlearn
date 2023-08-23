from django.contrib import admin
from nested_inline.admin import NestedModelAdmin, NestedStackedInline

from .models import (
    Assessment,
    Choice,
    Course,
    Lesson,
    Question,
    Subject,
    Content,
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


class ContentInline(NestedStackedInline):
    model = Content
    extra = 1
    fk_name = "lesson"


class LessonInline(NestedStackedInline):
    model = Lesson
    extra = 2
    fk_name = "course"
    inlines = [ContentInline]


@admin.register(Lesson)
class LessonAdmin(NestedModelAdmin):
    inlines = [ContentInline]


@admin.register(Course)
class CourseAdmin(NestedModelAdmin):
    list_display = ["id", "title", "subject", "created_at"]
    list_filter = ["created_at", "subject"]
    search_fields = ["title", "overview"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


class ChoiceInline(NestedStackedInline):
    model = Choice
    fk_name = "question"
    min_num = 4
    max_num = 4


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 3
    fk_name = "assessment"
    inlines = [ChoiceInline]


@admin.register(Assessment)
class AssessmentAdmin(NestedModelAdmin):
    list_display = ["id", "title", "course", "created_at"]
    list_filter = ["created_at", "course"]
    search_fields = ["title", "description"]
    inlines = [QuestionInline]


admin.site.register(Content)
