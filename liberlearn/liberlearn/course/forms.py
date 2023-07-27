from django.forms.models import inlineformset_factory

from .models import Course, Lesson

LessonFormSet = inlineformset_factory(
    Course, Lesson, fields=["title", "description"], extra=2, can_delete=True
)
