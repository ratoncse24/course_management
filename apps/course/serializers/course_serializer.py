from rest_framework import serializers
from apps.course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    """
        Serializer class for Course Model
    """
    class Meta:
        model = Course
        fields = ('course_id', 'title', 'description', 'instructor', 'duration', 'price')
