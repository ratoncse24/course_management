from django.db import models


# Course model which will store course data
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.CharField(max_length=255, db_index=True)
    duration = models.PositiveIntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'courses'
