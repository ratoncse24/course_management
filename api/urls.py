from django.urls import path, include


# Put here all apps url
urlpatterns = [
    path('', include('apps.course.urls')),
    path('', include('apps.enrollment.urls'))
]
