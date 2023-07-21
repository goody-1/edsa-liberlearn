from rest_framework import exceptions
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from liberlearn.accounts.models import User

from .models import Course, Module, Subject


class SubjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "title", "slug")
        extra_kwargs = {"url": {"view_name": "subject-detail", "lookup_field": "pk"}}

    def validate(self, data):
        if data["title"].lower() in [
            sub.title.lower() for sub in Subject.objects.all()
        ]:
            raise exceptions.ValidationError(
                detail="The subject title must not conflict with any other subject \
title in the database"
            )  # NOQA
        return data

    def create(self, validated_data):
        subject = Subject.objects.create(**validated_data)
        return subject

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.save()
        return instance


class CourseSerializer(HyperlinkedModelSerializer):
    mentor = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    subject = SerializerMethodField()

    def get_subject(self, course):
        # Use the SubjectSerializer to represent the subject in the serialized output
        serializer = SubjectSerializer(course.subject)
        return serializer.data

    class Meta:
        model = Course
        fields = ("id", "title", "overview", "slug", "created_at", "subject", "mentor")
        extra_kwargs = {"url": {"view_name": "course-detail", "lookup_field": "pk"}}


class ModuleSerializer(HyperlinkedModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = Module
        fields = "__all__"
        extra_kwargs = {"url": {"view_name": "module-detail", "lookup_field": "pk"}}
