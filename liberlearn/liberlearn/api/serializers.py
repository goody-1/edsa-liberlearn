from rest_framework import exceptions
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    PrimaryKeyRelatedField,
    RelatedField,
)

from liberlearn.accounts.models import User

from ..course.models import Content, Course, Lesson, Subject


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


class ItemRelatedField(RelatedField):
    def to_representation(self, value):
        return value.render()


class ContentSerializer(ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ["order", "item"]


class LessonWithContentsSerializer(ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ["order", "title", "description", "contents"]


class CourseWithContentsSerializer(ModelSerializer):
    lessons = LessonWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "subject",
            "title",
            "slug",
            "overview",
            "created",
            "owner",
            "lessons",
        ]


# class ContentSerializer(HyperlinkedModelSerializer):
#     item = SerializerMethodField()

#     def get_item(self, obj):
#         if isinstance(obj.item, Text):
#             return TextSerializer(obj.item).data
#         elif isinstance(obj.item, File):
#             return FileSerializer(obj.item).data
#         elif isinstance(obj.item, Image):
#             return ImageSerializer(obj.item).data
#         elif isinstance(obj.item, Video):
#             return VideoSerializer(obj.item).data

#     class Meta:
#         model = Content
#         fields = "__all__"
