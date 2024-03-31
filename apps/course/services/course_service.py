from rest_framework.exceptions import ValidationError

from apps.course.models import Course
from apps.enrollment.models import Enrollment


class CourseService:
    @staticmethod
    def create_course(data):
        """
        Create a new Course with the provided data.
        """
        return Course.objects.create(**data)

    @staticmethod
    def get_courses(filters=None):
        """
        Get courses with optional filtering.
        """
        queryset = Course.objects.all()
        if filters:
            try:
                queryset = queryset.filter(**filters)
            except Exception as e:
                return None, str(e)
        return queryset, None

    @staticmethod
    def get_course_by_id(id=None):
        """
        Get courses with provided course ID
        """
        try:
            queryset = Course.objects.get(course_id=id)
        except Course.DoesNotExist:
            return None, 'This course does not exist.'

        return queryset, None


    @staticmethod
    def get_course_enrollments(course_id=None):
        """
        Get course enrollment with provided course_id
        """
        return Enrollment.objects.filter(course_id=course_id)


