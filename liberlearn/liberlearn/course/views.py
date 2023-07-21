from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets

# from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Course, Module, Subject
from .permissions import IsAdminOrAuthenticatedReadOnly
from .serializers import CourseSerializer, ModuleSerializer, SubjectSerializer


class SubjectView(viewsets.ModelViewSet):
    """
    A simple viewset for viewing all subjects
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    http_method_names = ["get", "post", "patch"]
    lookup_field = "pk"

    def get_serializer_context(self):
        return {"request": self.request}

    @extend_schema(responses=serializer_class)
    def list(self, request):
        """List of all subjects"""

        serializer = self.serializer_class(
            self.queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @extend_schema(responses=serializer_class)
    def retrieve(self, request, pk=None):
        """Specific subject"""
        subject = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(subject, context={"request": request})
        return Response(serializer.data)

    @extend_schema(responses=serializer_class)
    def update(self, request, pk=None, *args, **kwargs):
        """Update specific subject"""
        # user = request.user
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(
            instance=instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseView(viewsets.ModelViewSet):
    """
    A simple viewset for viewing all Courses
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    http_method_names = ["get", "post", "patch"]
    lookup_field = "pk"

    def get_serializer_context(self):
        return {"request": self.request}

    @extend_schema(responses=serializer_class)
    def list(self, request):
        """List of all courses"""

        serializer = self.serializer_class(
            self.queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @extend_schema(responses=serializer_class)
    def retrieve(self, request, pk=None):
        """Specific course"""

        course = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(course, context={"request": request})
        return Response(serializer.data)

    # @extend_schema(responses=CourseSerializer)
    # def partial_update(self, request, pk=None):
    #     course = get_object_or_404(self.queryset, pk=pk)
    #     serializer = CourseSerializer(course)
    #     return Response(serializer.data)


class ModuleView(viewsets.ModelViewSet):
    """
    A simple viewset for viewing all Modules
    """

    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (IsAdminOrAuthenticatedReadOnly,)
    http_method_names = ["get", "post", "patch"]
    lookup_field = "pk"

    def get_serializer_context(self):
        return {"request": self.request}

    @extend_schema(responses=serializer_class)
    def list(self, request):
        """List of all modules"""
        serializer = self.serializer_class(
            self.queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @extend_schema(responses=serializer_class)
    def retrieve(self, request, pk=None):
        """Specific module"""
        module = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(module, context={"request": request})
        return Response(serializer.data)

    # @extend_schema(responses=ModuleSerializer)
    # def partial_update(self, request, pk=None):
    #     module = get_object_or_404(self.queryset, pk=pk)
    #     serializer = ModuleSerializer(module)
    #     return Response(serializer.data)
