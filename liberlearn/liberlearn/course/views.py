# from django.shortcuts import get_object_or_404
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

# from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.db.models import Count
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from liberlearn.students.forms import CourseEnrollForm

from .forms import LessonFormSet
from .models import Content, Course, Lesson, Subject
from .permissions import IsAdminOrReadOnly
from .serializers import (
    ContentSerializer,
    CourseCreateSerializer,
    CourseListSerializer,
    LessonCreateSerializer,
    LessonListSerializer,
    SubjectSerializer,
)

# from students.forms import CourseEnrollForm

# from rest_framework.response import Response


class SubjectView(viewsets.ModelViewSet):
    """
    The Subject viewset, perform CRUD operations based on privileges
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "pk"

    def get_serializer_context(self):
        return {"request": self.request}

    @extend_schema(responses=serializer_class(many=True))
    def list(self, request):
        """
        Return a list of all subjects.

        Returns:
            Response: List of subjects.
        """
        return super().list(request)

    @extend_schema(responses=serializer_class)
    def retrieve(self, request, pk=None):
        """
        Return a specific subject.

        Parameters:
            id (int): The primary key of the subject.

        Returns:
            Response: Serialized subject data.
        """
        return super().retrieve(request, pk)

    @extend_schema(responses=serializer_class)
    def create(self, request, *args, **kwargs):
        """
        Create a new subject.

        Parameters:
            request (Request): The HTTP request.

        Returns:
            Response: Serialized subject data.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(responses=serializer_class)
    def update(self, request, pk=None, *args, **kwargs):
        """
        Update an existing subject.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the subject.

        Returns:
            Response: Serialized subject data.
        """
        return super().update(request, pk, *args, **kwargs)

    @extend_schema(responses=serializer_class)
    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partially update an existing subject.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the subject.

        Returns:
            Response: Serialized subject data.
        """
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(responses={204: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete an existing subject.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the subject.

        Returns:
            Response: Success message or Not found error.
        """
        return super().destroy(request, pk, *args, **kwargs)


class CourseView(viewsets.ModelViewSet):
    """
    The Course viewset, perform CRUD operations based on your privileges
    """

    queryset = Course.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CourseListSerializer
        return CourseCreateSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    @extend_schema(responses=CourseListSerializer(many=True))
    def list(self, request):
        """
        Return a list of all courses.

        Returns:
            Response: List of courses.
        """
        return super().list(request)

    @extend_schema(responses=CourseListSerializer)
    def retrieve(self, request, pk=None):
        """
        Return a specific course.

        Parameters:
            id (int): The primary key of the course.

        Returns:
            Response: Serialized course data.
        """
        return super().retrieve(request, pk)

    @extend_schema(responses=CourseCreateSerializer)
    def create(self, request, *args, **kwargs):
        """
        Create a new course.

        Parameters:
            request (Request): The HTTP request.

        Returns:
            Response: Serialized course data.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(responses=CourseCreateSerializer)
    def update(self, request, pk=None, *args, **kwargs):
        """
        Update an existing course.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the course.

        Returns:
            Response: Serialized course data.
        """
        return super().update(request, pk, *args, **kwargs)

    @extend_schema(responses=CourseCreateSerializer)
    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partially update an existing course.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the course.

        Returns:
            Response: Serialized course data.
        """
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(responses={204: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete an existing course.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the course.

        Returns:
            Response: Success message or Not found error.
        """
        return super().destroy(request, pk, *args, **kwargs)


class LessonView(viewsets.ModelViewSet):
    """
    A simple viewset for viewing all Lessons
    """

    queryset = Lesson.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return LessonListSerializer
        return LessonCreateSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    @extend_schema(responses=LessonListSerializer)
    def list(self, request):
        """
        Return a list of all lessons.

        Returns:
            Response: List of lessons.
        """
        return super().list(request)

    @extend_schema(responses=LessonListSerializer)
    def retrieve(self, request, pk=None):
        """
        Return a specific lesson.

        Parameters:
            id (int): The primary key of the lesson.

        Returns:
            Response: Serialized lesson data.
        """
        return super().retrieve(request, pk)

    @extend_schema(responses=LessonCreateSerializer)
    def create(self, request, *args, **kwargs):
        """
        Create a new lesson.

        Parameters:
            request (Request): The HTTP request.

        Returns:
            Response: Serialized lesson data.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(responses=LessonCreateSerializer)
    def update(self, request, pk=None, *args, **kwargs):
        """
        Update an existing lesson.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the lesson.

        Returns:
            Response: Serialized lesson data.
        """
        return super().update(request, pk, *args, **kwargs)

    @extend_schema(responses=LessonCreateSerializer)
    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partially update an existing lesson.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the lesson.

        Returns:
            Response: Serialized lesson data.
        """
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(responses={204: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete an existing lesson.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the lesson.

        Returns:
            Response: Success message or Not found error.
        """
        return super().destroy(request, pk, *args, **kwargs)


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
