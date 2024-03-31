from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.course.models import Course
from apps.enrollment.models import Enrollment
from apps.course.serializers.course_serializer import CourseSerializer
from apps.enrollment.serializers.enrollment_serializer import EnrollmentSerializer
from datetime import datetime

class CourseApiTestCase(TestCase):
    """
    Test cases for the Course API endpoints.
    """
    def setUp(self):
        """
            Set up test data and client for API testing.
        """
        self.client = APIClient()
        self.course_data = {
            'title': 'Test Course',
            'description': 'This is a test course',
            'instructor': 'Raton',
            'duration': 5,
            'price': 99.99
        }
        self.invalid_course_data_for_empty_title = {
            'title': '', # invalid title
            'description': 'This is a test course',
            'instructor': 'Habib',
            'duration': 4,
            'price': 99.99
        }
        self.invalid_course_data = {
            'title': 'Test Course - Failed',
            'description': 'This is a test course',
            'instructor': 'Habib',
            'duration': -5,  # Invalid duration
            'price': 99.99
        }
        self.course = Course.objects.create(**self.course_data)

    def test_create_course(self):
        """
               Test API endpoint to create a new course.
        """
        response = self.client.post(reverse('course-list'), data=self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)  # Two courses now in the database

    def test_create_invalid_course_for_empty_title(self):
        """
                Test API endpoint to create a course with an empty title.
         """
        response = self.client.post(reverse('course-list'), data=self.invalid_course_data_for_empty_title)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 1)  # No new course added

    def test_create_invalid_course_for_invalid_duration(self):
        """
                Test API endpoint to create a course with an invalid duration value.
        """
        response = self.client.post(reverse('course-list'), data=self.invalid_course_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 1)  # No new course added

    def test_get_courses(self):
        """
                Test API endpoint to retrieve a list of courses.
        """
        response = self.client.get(reverse('course-list'))
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class CourseDetailAPIViewTestCase(TestCase):
    """
        Test cases for the Course detail API endpoint.
    """
    def setUp(self):
        """
                Set up test data and client for API testing.
        """
        self.client = APIClient()
        self.course = Course.objects.create(
            title='Test Course',
            description='This is a test course',
            instructor='Raton',
            duration=5,
            price=99.99
        )
        self.enrollment = Enrollment.objects.create(
            student_name='Sumon',
            course_id=self.course,
            enrollment_date=datetime.now().date()
        )

    def test_get_course_details_with_enrollments(self):
        """
                Test API endpoint to retrieve detailed course information with associated enrollments.
        """
        response = self.client.get(reverse('course-detail', kwargs={'id': self.course.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('course_details', response.data)
        self.assertIn('student_enrollments', response.data)
        self.assertEqual(response.data['course_details']['title'], 'Test Course')
        self.assertEqual(len(response.data['student_enrollments']), 1)

    def test_get_invalid_course_details_with_enrollments(self):
        """
        Test API endpoint to retrieve course details with invalid course ID.
        """
        response = self.client.get(reverse('course-detail', kwargs={'id': self.course.pk + 7000 }))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
