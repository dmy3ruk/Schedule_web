# school_shedule/urls.py
from django.contrib import admin
from django.urls import path
from school_shedule.views import  ScheduleView,HomeMonth

urlpatterns = [
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('', HomeMonth.as_view(), name=''),

]
