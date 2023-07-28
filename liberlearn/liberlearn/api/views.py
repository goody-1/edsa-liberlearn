from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..course.models import Course, Subject
from .permissions import IsAdminOrReadOnly, IsEnrolled
from .serializers import (  # LessonCreateSerializer,; LessonListSerializer,; ContentSerializer,
    CourseCreateSerializer,
    CourseListSerializer,
    CourseWithContentsSerializer,
    SubjectSerializer,
)


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

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({"enrolled": True})

    @action(
        detail=True,
        methods=["get"],
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled],
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

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


class CourseEnrollView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        course.students.add(request.user)
        return Response({"enrolled": True})


# class LessonView(viewsets.ModelViewSet):
#     """
#     A simple viewset for viewing all Lessons
#     """

#     queryset = Lesson.objects.all()
#     permission_classes = (IsAdminOrReadOnly,)
#     http_method_names = ["get", "post", "patch", "delete"]
#     lookup_field = "pk"

#     def get_serializer_class(self):
#         if self.request.method in SAFE_METHODS:
#             return LessonListSerializer
#         return LessonCreateSerializer

#     def get_serializer_context(self):
#         return {"request": self.request}

#     @extend_schema(responses=LessonListSerializer)
#     def list(self, request):
#         """
#         Return a list of all lessons.

#         Returns:
#             Response: List of lessons.
#         """
#         return super().list(request)

#     @extend_schema(responses=LessonListSerializer)
#     def retrieve(self, request, pk=None):
#         """
#         Return a specific lesson.

#         Parameters:
#             id (int): The primary key of the lesson.

#         Returns:
#             Response: Serialized lesson data.
#         """
#         return super().retrieve(request, pk)

#     @extend_schema(responses=LessonCreateSerializer)
#     def create(self, request, *args, **kwargs):
#         """
#         Create a new lesson.

#         Parameters:
#             request (Request): The HTTP request.

#         Returns:
#             Response: Serialized lesson data.
#         """
#         return super().create(request, *args, **kwargs)

#     @extend_schema(responses=LessonCreateSerializer)
#     def update(self, request, pk=None, *args, **kwargs):
#         """
#         Update an existing lesson.

#         Parameters:
#             request (Request): The HTTP request.
#             id (int): The primary key of the lesson.

#         Returns:
#             Response: Serialized lesson data.
#         """
#         return super().update(request, pk, *args, **kwargs)

#     @extend_schema(responses=LessonCreateSerializer)
#     def partial_update(self, request, pk=None, *args, **kwargs):
#         """
#         Partially update an existing lesson.

#         Parameters:
#             request (Request): The HTTP request.
#             id (int): The primary key of the lesson.

#         Returns:
#             Response: Serialized lesson data.
#         """
#         return super().partial_update(request, pk, *args, **kwargs)

#     @extend_schema(responses={204: None})
#     def destroy(self, request, pk=None, *args, **kwargs):
#         """
#         Delete an existing lesson.

#         Parameters:
#             request (Request): The HTTP request.
#             id (int): The primary key of the lesson.

#         Returns:
#             Response: Success message or Not found error.
#         """
#         return super().destroy(request, pk, *args, **kwargs)
