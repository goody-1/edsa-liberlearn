from rest_framework import exceptions
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    PrimaryKeyRelatedField,
    RelatedField,
    SerializerMethodField,
)

from liberlearn.accounts.models import User

from ..course.models import Content, Course, Lesson, Subject


class SubjectSerializer(HyperlinkedModelSerializer):
    courses = SerializerMethodField()

    class Meta:
        model = Subject
        fields = ("id", "url", "title", "slug", "courses")
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

    def get_courses(self, subject):
        courses = Course.objects.filter(subject=subject)
        serializer = CourseListSerializer(
            courses, many=True, context=self.context
        )
        return serializer.data


class CourseListSerializer(HyperlinkedModelSerializer):
    mentor = PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    lessons = SerializerMethodField()
    number_of_students = SerializerMethodField()

    # subject = SubjectSerializer() # This avoids the
    # `RecursionError: maximum recursion depth exceeded` error

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
            "number_of_students",
            "lessons",
        )
        extra_kwargs = {
            "url": {"view_name": "course-detail", "lookup_field": "pk"}
        }

    def get_lessons(self, course):
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonWithContentsSerializer(
            lessons, many=True, context=self.context
        )
        return serializer.data

    def get_number_of_students(self, course):
        number_of_students = len(course.students.all())
        return number_of_students


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
