from django import forms

from liberlearn.course.models import Course


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), widget=forms.HiddenInput
    )
