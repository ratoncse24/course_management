from rest_framework import serializers
from apps.enrollment.models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    """
        Serializer class for Enrollment Model
    """
    class Meta:
        model = Enrollment
        fields = ('enrollment_id', 'student_name', 'course_id', 'enrollment_date', )
