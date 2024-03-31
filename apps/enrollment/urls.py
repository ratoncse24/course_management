from rest_framework import routers

from django.urls import path

from apps.enrollment.views import EnrollmentApi

urlpatterns = [
    path('enrollments', EnrollmentApi.as_view(), name='enrollment-list'),
]