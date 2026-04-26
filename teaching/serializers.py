from rest_framework import serializers
from teaching.models import Course, Lesson

class CourseSerializer(serializers.ModelSerializer):

    count_lessons = serializers.SerializerMethodField()

    @staticmethod
    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = "__all__"

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"