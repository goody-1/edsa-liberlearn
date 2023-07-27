from rest_framework import exceptions
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
)

from liberlearn.accounts.models import User

from .models import Content, Course, File, Image, Lesson, Subject, Text, Video


class SubjectSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ("id", "url", "title", "slug")
        extra_kwargs = {
            "url": {"view_name": "subject-detail", "lookup_field": "pk"}
        }

    def validate(self, data):
        if data["title"].lower() in [
            sub.title.lower() for sub in Subject.objects.all()
        ]:
            raise exceptions.ValidationError(
                detail="The subject title must not conflict with any other \
subject title in the database"
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
        extra_kwargs = {
            "url": {"view_name": "course-detail", "lookup_field": "pk"}
        }


class CourseCreateSerializer(HyperlinkedModelSerializer):
    mentor = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    subject = PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
    )

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "overview",
            "slug",
            "created_at",
            "subject",
            "mentor",
        )


class LessonListSerializer(HyperlinkedModelSerializer):
    course = CourseListSerializer()

    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            "url": {"view_name": "lesson-detail", "lookup_field": "pk"}
        }


class LessonCreateSerializer(HyperlinkedModelSerializer):
    course = PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
    )

    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            "url": {"view_name": "lesson-detail", "lookup_field": "pk"}
        }


class TextSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"


class FileSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class ImageSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class VideoSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class ContentSerializer(HyperlinkedModelSerializer):
    item = SerializerMethodField()

    def get_item(self, obj):
        if isinstance(obj.item, Text):
            return TextSerializer(obj.item).data
        elif isinstance(obj.item, File):
            return FileSerializer(obj.item).data
        elif isinstance(obj.item, Image):
            return ImageSerializer(obj.item).data
        elif isinstance(obj.item, Video):
            return VideoSerializer(obj.item).data

    class Meta:
        model = Content
        fields = "__all__"
