from django.db import models

class Lesson(models.Model):
    subject = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    day_of_week = models.DateField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.class_name} - {self.subject} ({self.day_of_week})'
