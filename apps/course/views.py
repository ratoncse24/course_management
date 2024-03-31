from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.course.models import Course
from apps.course.serializers.course_serializer import CourseSerializer
from apps.course.services.course_service import CourseService
from apps.enrollment.serializers.enrollment_serializer import EnrollmentSerializer


class CourseApi(APIView):
  """
  API endpoint for managing courses.

  This API allows users to retrieve a list of courses and create new courses.
  """
  def get(self, request, *args, **kwargs):
    """
    Retrieve a list of courses.

    Returns:
        Response: List of course details.
    """
    filters = request.query_params.dict()
    courses, error = CourseService.get_courses(filters)
    if error:
      return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)


  def post(self, request):
    """
    Create a new course.

    Args:
        request (Request): HTTP POST request containing course data.

    Returns:
        Response: Created course details.
    """
    create_serializer = CourseSerializer(data=request.data)

    if create_serializer.is_valid():

      course_object = CourseService.create_course(create_serializer.validated_data)

      read_serializer = CourseSerializer(course_object)

      return Response(read_serializer.data, status=201)

    return Response(create_serializer.errors, status=400)



class CourseDetailAPIView(APIView):
  """
  API endpoint for retrieving course details with associated enrollments.

  This API allows users to retrieve detailed information about a specific course
  along with the enrollments for that course.
  """
  def get(self, *args, **kwargs):
    """
    Retrieve detailed information about a specific course with associated enrollments.

    Args:
        *args: Additional arguments.
        **kwargs: Additional keyword arguments containing the course ID.

    Returns:
        Response: Detailed course information with associated enrollments.
    """
    course_detail, error = CourseService.get_course_by_id(id=kwargs.get('id'))
    if error:
      return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    course_serializer = CourseSerializer(course_detail)

    # Retrieve enrollments for the course
    enrollments = CourseService.get_course_enrollments(course_detail.course_id)
    enrollment_serializer = EnrollmentSerializer(enrollments, many=True)

    # Combine course details and enrollments in the response
    response_data = {
      'course_details': course_serializer.data,
      'student_enrollments': enrollment_serializer.data
    }
    return Response(response_data)
