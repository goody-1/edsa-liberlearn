from rest_framework import exceptions
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    PrimaryKeyRelatedField,
)

from liberlearn.accounts.models import User

from .models import Course, Module, Subject


class SubjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "url", "title", "slug")
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


class CourseListSerializer(HyperlinkedModelSerializer):
    mentor = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    subject = SubjectSerializer()

    class Meta:
        model = Course
        fields = (
            "id",
            "url",
            "title",
            "overview",
            "slug",
            "created_at",
            "subject",
            "mentor",
        )
        extra_kwargs = {"url": {"view_name": "course-detail", "lookup_field": "pk"}}


class CourseCreateSerializer(HyperlinkedModelSerializer):
    mentor = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    subject = PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
    )

    class Meta:
        model = Course
        fields = ("id", "title", "overview", "slug", "created_at", "subject", "mentor")


class ModuleListSerializer(HyperlinkedModelSerializer):
    course = CourseListSerializer()

    class Meta:
        model = Module
        fields = "__all__"
        extra_kwargs = {"url": {"view_name": "module-detail", "lookup_field": "pk"}}


class ModuleCreateSerializer(HyperlinkedModelSerializer):
    course = PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
    )

    class Meta:
        model = Module
        fields = "__all__"
        extra_kwargs = {"url": {"view_name": "module-detail", "lookup_field": "pk"}}
