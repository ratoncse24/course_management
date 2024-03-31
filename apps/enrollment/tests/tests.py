from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.course.models import Course
from apps.enrollment.models import Enrollment

class EnrollmentApiTestCase(TestCase):
    """
    Test cases for the Enrollment API endpoint.
    """
    def setUp(self):
        """
        Set up test data and client for API testing.
        """
        self.client = APIClient()
        # Get today's date
        today_date = datetime.now().date()
        # Generate a previous date
        previous_date = today_date - timedelta(days=1)

        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            instructor='John Doe',
            duration=5,
            price=99.99
        )
        # when all enrollment data are valid
        self.valid_enrollment_data = {
            'student_name': 'Raton',
            'course_id': self.course.course_id,
            'enrollment_date': str(today_date)
        }
        self.invalid_enrollment_data_for_enrollment_date = {
            'student_name': 'Habib',
            'course_id': self.course.course_id,
            'enrollment_date': str(previous_date) # Invalid enrollment_date. Date can't be less than today
        }
        self.invalid_enrollment_data_for_invalid_course_reference = {
            'student_name': 'Raton Hosen',
            'course_id': self.course.course_id+60000, # Invalid course id which is not exist in the database
            'enrollment_date': str(today_date)
        }

        self.invalid_enrollment_data_for_invalid_student_name = {
            'student_name': 'Raton #@#$$$$$',  # Invalid student name. containing special character
            'course_id': self.course.course_id,
            'enrollment_date': str(today_date)
        }
        self.invalid_enrollment_data_student_name_empty = {
            'student_name': '',  # Invalid empty student name
            'course_id': self.course.course_id,
            'enrollment_date': str(today_date)
        }

    def test_create_valid_enrollment(self):
        """
        Test API endpoint to create a valid enrollment.
        """
        response = self.client.post(reverse('enrollment-list'), data=self.valid_enrollment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) # verify the status code are expected
        self.assertTrue(Enrollment.objects.filter(student_name='Raton').exists())  # Verify enrollment is created

    def test_create_invalid_enrollment_for_enrollment_date(self):
        """
        Test API endpoint to create an enrollment with an invalid enrollment date.
        """
        response = self.client.post(reverse('enrollment-list'), data=self.invalid_enrollment_data_for_enrollment_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Enrollment.objects.filter(student_name='').exists())  # Verify no invalid enrollment is created

    def test_create_invalid_enrollment_for_invalid_course_reference(self):
        """
        Test API endpoint to create an enrollment with an invalid course reference.
        """
        response = self.client.post(reverse('enrollment-list'), data=self.invalid_enrollment_data_for_invalid_course_reference)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Enrollment.objects.filter(student_name='').exists())  # Verify no invalid enrollment is created

    def test_create_invalid_enrollment_for_invalid_student_name(self):
        """
        Test API endpoint to create an enrollment with an invalid student name containing special characters.
        """
        response = self.client.post(reverse('enrollment-list'), data=self.invalid_enrollment_data_for_invalid_student_name)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Enrollment.objects.filter(student_name='').exists())  # Verify no invalid enrollment is created

    def test_create_invalid_enrollment(self):
        """
        Test API endpoint to create an enrollment with an empty student name.
        """
        response = self.client.post(reverse('enrollment-list'), data=self.invalid_enrollment_data_student_name_empty)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Enrollment.objects.filter(student_name='').exists())  # Verify no invalid enrollment is created
