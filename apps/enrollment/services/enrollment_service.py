from datetime import datetime

from rest_framework.exceptions import ValidationError

from apps.enrollment.models import Enrollment

class EnrollmentService:
    @staticmethod
    def enroll_student(data):
        """
        Create a new Course Enrollment with the provided data.
        """
        return Enrollment.objects.create(**data)

    @staticmethod
    def validate_enrollment(data):
        """
        Validate the enrollment data before creation.
        """
        try:
            Enrollment(**data).full_clean()

            # custom validation goes here...

            if not data.get('student_name').replace(' ', '').isalnum():
                return False, "Student name can not contain any special character"

            if data.get('student_name').isdigit():
                return False, "Student name must starts with a alphabetic character"

            if data.get('enrollment_date') < datetime.now().date():
                return False, "Enrollment date must be greater then or equal to today"

        except ValidationError as e:
            # Handle validation error
            return False, e.messages
        return True, None
