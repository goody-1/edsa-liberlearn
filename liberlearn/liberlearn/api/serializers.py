from rest_framework import exceptions
from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
    PrimaryKeyRelatedField,
    RelatedField,
    SerializerMethodField,
)

from liberlearn.accounts.models import User

from ..course.models import (
    Assessment,
    Choice,
    Content,
    Course,
    Lesson,
    Question,
    Subject,
    Text,
    Video,
    Image,
    File,
)


class SubjectSerializer(HyperlinkedModelSerializer):
    courses = SerializerMethodField()
    number_of_courses = SerializerMethodField()

    class Meta:
        model = Subject
        fields = (
            "id",
            "url",
            "title",
            "info",
            "image_link",
            "intro_video",
            "slug",
            "number_of_courses",
            "courses",
        )
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

    def get_courses(self, subject: Subject):
        courses = Course.objects.filter(subject=subject)
        serializer = CourseListSerializer(
            courses, many=True, context=self.context
        )
        return serializer.data

    def get_number_of_courses(self, subject: Subject):
        number_of_courses = len(subject.courses.all())
        return number_of_courses


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

    def get_lessons(self, course: Course):
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonWithContentsSerializer(
            lessons, many=True, context=self.context
        )
        return serializer.data

    def get_number_of_students(self, course: Course):
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
    item = SerializerMethodField()
    content_type = SerializerMethodField()

    class Meta:
        model = Content
        fields = ["id", "order", "item", "content_type"]

    def get_content_type(self, content: Content):
        hld = str(type(content.item)).split(".")[-1]
        content_type = hld[:-2]
        return content_type

    def get_item(self, content):
        # Determine the item's type and get the URL dynamically
        item = content.item
        if isinstance(item, Text):
            return item.get_item_url()
        elif isinstance(item, Image):
            return item.get_item_url()
        elif isinstance(item, Video):
            return item.get_item_url()
        elif isinstance(item, File):
            return item.get_item_url()
        else:
            return None


class LessonWithContentsSerializer(ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ["id", "order", "title", "description", "contents"]


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


class ChoiceSerializer(ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "text", "is_correct")


class QuestionSerializer(ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ("id", "text", "choices")

    def create(self, validated_data):
        choices_data = validated_data.pop("choices")
        question = Question.objects.create(**validated_data)

        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)

        return question


class AssessmentSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Assessment
        fields = (
            "id",
            "course",
            "title",
            "description",
            "created_at",
            "questions",
        )

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        assessment = Assessment.objects.create(**validated_data)

        for question_data in questions_data:
            choices_data = question_data.pop("choices")
            question = Question.objects.create(**question_data)

            for choice_data in choices_data:
                question.choices.create(**choice_data)

        return assessment


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
