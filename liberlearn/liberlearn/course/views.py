# from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS

from .models import Course, Module, Subject
from .permissions import IsAdminOrAuthenticatedReadOnly
from .serializers import (
    CourseCreateSerializer,
    CourseListSerializer,
    ModuleCreateSerializer,
    ModuleListSerializer,
    SubjectSerializer,
)

# from rest_framework.response import Response


class SubjectView(viewsets.ModelViewSet):
    """
    The Subject viewset, perform CRUD operations based on privileges
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
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
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
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


class ModuleView(viewsets.ModelViewSet):
    """
    A simple viewset for viewing all Modules
    """

    queryset = Module.objects.all()
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ModuleListSerializer
        return ModuleCreateSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    @extend_schema(responses=ModuleListSerializer)
    def list(self, request):
        """
        Return a list of all module.

        Returns:
            Response: List of module.
        """
        return super().list(request)

    @extend_schema(responses=ModuleListSerializer)
    def retrieve(self, request, pk=None):
        """
        Return a specific module.

        Parameters:
            id (int): The primary key of the module.

        Returns:
            Response: Serialized module data.
        """
        return super().retrieve(request, pk)

    @extend_schema(responses=ModuleCreateSerializer)
    def create(self, request, *args, **kwargs):
        """
        Create a new module.

        Parameters:
            request (Request): The HTTP request.

        Returns:
            Response: Serialized module data.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(responses=ModuleCreateSerializer)
    def update(self, request, pk=None, *args, **kwargs):
        """
        Update an existing module.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the module.

        Returns:
            Response: Serialized module data.
        """
        return super().update(request, pk, *args, **kwargs)

    @extend_schema(responses=ModuleCreateSerializer)
    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        Partially update an existing module.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the module.

        Returns:
            Response: Serialized module data.
        """
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(responses={204: None})
    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete an existing module.

        Parameters:
            request (Request): The HTTP request.
            id (int): The primary key of the module.

        Returns:
            Response: Success message or Not found error.
        """
        return super().destroy(request, pk, *args, **kwargs)
