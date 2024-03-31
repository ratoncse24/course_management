from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.enrollment.serializers.enrollment_serializer import EnrollmentSerializer
from apps.enrollment.models import Enrollment
from apps.enrollment.services.enrollment_service import EnrollmentService


class EnrollmentApi(APIView):
  """
  API endpoint for enrolling students to courses.

  This API allows users to enroll students to courses by providing the necessary enrollment data.
  """
  def post(self, request, *args, **kwargs):
    """
    Create a new enrollment.

    Args:
        request (Request): HTTP POST request containing enrollment data.

    Returns:
        Response: Created enrollment details or error response.
    """
    serializer = EnrollmentSerializer(data=request.data)
    if serializer.is_valid():
      is_valid, validation_errors = EnrollmentService.validate_enrollment(serializer.validated_data)
      if is_valid:
        # Data is valid, proceed with creation
        EnrollmentService.enroll_student(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      else:
        # Data is invalid, return error response
        return Response({'errors': validation_errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
