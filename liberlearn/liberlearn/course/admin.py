from django.contrib import admin

from .models import Course, Lesson, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


class LessonInline(admin.StackedInline):
    model = Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "subject", "created_at"]
    list_filter = ["created_at", "subject"]
    search_fields = ["title", "overview"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


# admin.site.register(Lesson)
# admin.site.register(Content)
