from django.shortcuts import get_object_or_404

# from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from ..course.models import Assessment, Course, Question, Subject
from .permissions import IsAdminOrReadOnly, IsEnrolled
from .serializers import (  # LessonCreateSerializer,; LessonListSerializer,; ContentSerializer,
    AssessmentSerializer,
    CourseCreateSerializer,
    CourseListSerializer,
    CourseWithContentsSerializer,
    QuestionSerializer,
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
        permission_classes=[IsAuthenticated],  # IsEnrolled
    )
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


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


class AssessmentView(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "pk"

    def get_serializer_context(self):
        return {"request": self.request}


class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = "pk"

    def get_serializer_context(self):
        return {"request": self.request}
