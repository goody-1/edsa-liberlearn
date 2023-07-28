from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.core.cache import cache
from django.db.models import Count
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from liberlearn.students.forms import CourseEnrollForm

from .forms import LessonFormSet
from .models import Content, Course, Lesson, Subject

# from django.contrib.auth.views import LoginView
# from django.shortcuts import get_object_or_404
# from students.forms import CourseEnrollForm


class AdminMixin(AccessMixin):
    def handle_no_permission(self):
        messages.error(
            self.request, "You do not have permission to access this page."
        )
        return redirect(reverse("login"))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            # print(f"\n\n{request.user.is_staff}\n\n")
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ManagerMixin(AdminMixin, object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs


class ManagerEditMixin(object):
    def form_valid(self, form):
        return super().form_valid(form)


class ManagerCourseMixin(
    ManagerMixin, LoginRequiredMixin, PermissionRequiredMixin
):
    model = Course
    fields = ["subject", "title", "slug", "overview"]
    success_url = reverse_lazy("manage_course_list")


class ManagerCourseEditMixin(ManagerCourseMixin, ManagerEditMixin):
    template_name = "course/manage/course/form.html"


class ManageCourseListView(ManagerCourseMixin, ListView):
    template_name = "course/manage/course/list.html"
    permission_required = "course.view_course"


class CourseCreateView(ManagerCourseEditMixin, CreateView):
    permission_required = "course.add_course"


class CourseUpdateView(ManagerCourseEditMixin, UpdateView):
    permission_required = "course.change_course"


class CourseDeleteView(ManagerCourseMixin, DeleteView):
    template_name = "course/manage/course/delete.html"
    permission_required = "course.delete_course"


class CourseLessonUpdateView(AdminMixin, TemplateResponseMixin, View):
    template_name = "course/manage/lesson/formset.html"
    course = None

    def get_formset(self, data=None):
        return LessonFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {"course": self.course, "formset": formset}
        )

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_course_list")
        return self.render_to_response(
            {"course": self.course, "formset": formset}
        )


class ContentCreateUpdateView(AdminMixin, TemplateResponseMixin, View):
    lesson = None
    model = None
    obj = None
    template_name = "course/manage/content/form.html"

    def get_model(self, model_name):
        if model_name in ["text", "video", "image", "file"]:
            return apps.get_model(app_label="course", model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(
            model, exclude=["order", "created", "updated"]
        )
        return Form(*args, **kwargs)

    def dispatch(self, request, lesson_id, model_name, id=None):
        self.lesson = get_object_or_404(Lesson, id=lesson_id)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id)
        return super().dispatch(request, lesson_id, model_name, id)

    def get(self, request, lesson_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(self, request, lesson_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if not id:
                # new content
                Content.objects.create(lesson=self.lesson, item=obj)
            return redirect("lesson_content_list", self.lesson.id)

        return self.render_to_response({"form": form, "object": self.obj})


class ContentDeleteView(AdminMixin, View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id)
        lesson = content.lesson
        content.item.delete()
        content.delete()
        return redirect("lesson_content_list", lesson.id)


class LessonContentListView(TemplateResponseMixin, View):
    template_name = "course/manage/lesson/content_list.html"

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)

        return self.render_to_response({"lesson": lesson})


class LessonOrderView(
    CsrfExemptMixin, JsonRequestResponseMixin, View, AdminMixin
):
    def post(self, request):
        for id, order in self.request_json.items():
            Lesson.objects.filter(id=id).update(order=order)
        return self.render_json_response({"saved": "OK"})


class ContentOrderView(
    AdminMixin, CsrfExemptMixin, JsonRequestResponseMixin, View
):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id,
            ).update(order=order)
        return self.render_json_response({"saved": "OK"})


class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = "course/course/list.html"

    def get(self, request, subject=None):
        subjects = cache.get("all_subjects")
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count("courses"))
            cache.set("all_subjects", subjects)
        all_courses = Course.objects.annotate(total_lessons=Count("lessons"))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            key = f"subject_{subject.id}_courses"
            courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key, courses)
        else:
            courses = cache.get("all_courses")
            if not courses:
                courses = all_courses
                cache.set("all_courses", courses)
        return self.render_to_response(
            {"subjects": subjects, "subject": subject, "courses": courses}
        )


class CourseDetailView(DetailView):
    model = Course
    template_name = "course/course/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["enroll_form"] = CourseEnrollForm(
            initial={"course": self.object}
        )
        return context
