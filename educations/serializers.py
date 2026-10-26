from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from educations.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lesson = SerializerMethodField()
    lessons_list = LessonSerializer(source='lessons', read_only=True, many=True)

    def get_count_lesson(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
