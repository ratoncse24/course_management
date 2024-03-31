from rest_framework import routers

from django.urls import path

from apps.course.views import CourseApi, CourseDetailAPIView

urlpatterns = [
    path('courses', CourseApi.as_view(), name='course-list'),
    path('courses/<int:id>', CourseDetailAPIView.as_view(), name='course-detail'),
]