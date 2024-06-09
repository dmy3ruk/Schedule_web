from django.contrib import admin

from school_shedule.models import Lesson


# Register your models here.
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('subject', 'class_name', 'day_of_week', 'start_time', 'end_time', 'teacher')

admin.site.register(Lesson, LessonsAdmin)