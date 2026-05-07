from rest_framework import serializers
from teaching.models import Course, Lesson
from teaching.validators import youtube_validator

class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[youtube_validator])

    class Meta:
        model = Lesson
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    count_lessons = serializers.SerializerMethodField()

    def get_count_lessons(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = "__all__"