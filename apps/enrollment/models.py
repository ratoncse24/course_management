from venv import logger

from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.course.models import Course


# Enrollment model which will store course enrollments data
class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_course', db_index=True)
    enrollment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Student Name: {self.student_name}"

    class Meta:
        db_table = 'enrollments'
