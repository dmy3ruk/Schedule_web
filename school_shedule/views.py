import calendar
from datetime import datetime, timedelta, timezone
from operator import attrgetter

from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views import View

from school_shedule.forms import LoginForm
from school_shedule.models import Lesson


# Create your views here.
class ScheduleView(View):
    def get(self, request):

        return render(request, 'index.html')


class AuthView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'auth.html', {'loginForm': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')  # Замість 'index', переконайтеся, що маршрут 'home' правильно налаштований
        return render(request, 'auth.html', {'loginForm': form})


class HomeMonth(View):
    def get(self, request):
        tab = request.GET.get('tab', 'day')  # Default to 'month' if no tab is provided
        return self.render_schedule(request, tab)

    def post(self, request, *args, **kwargs):
        tab = request.GET.get('tab', 'day')  # Get the active tab from the query parameter
        return self.render_schedule(request, tab)

    def render_schedule(self, request, tab):
        sort = ''
        # Update the session variables if new values are posted
        if 'class_name' in request.POST:
            request.session['class'] = request.POST.get('class_name')

        if 'teacher_name' in request.POST:

            request.session['teacher'] = request.POST.get('teacher_name')
            sort = 'teacher'
        # Get the class and teacher names from the session, with default empty strings
        class_name = request.session.get('class', '')
        teacher_name = request.session.get('teacher', '')
        # Filter lessons based on class and teacher names
        numbers_lesson = ''
        lessons = Lesson.objects.all()
        if class_name:
            lessons = lessons.filter(class_name=class_name)
            numbers_lesson = lessons.count()
        if teacher_name:
            lessons = lessons.filter(teacher=teacher_name)
            sort = 'teacher'
            numbers_lesson = lessons.count()
        current_date = datetime.now()

        # Filter lessons based on the selected tab (month, week, or day)
        if tab == 'month':
            first_day = current_date.replace(day=1)
            last_day = current_date.replace(day=calendar.monthrange(current_date.year, current_date.month)[1])
            lessons_all = lessons.filter(day_of_week__gte=first_day, day_of_week__lte=last_day)
            numbers_lesson = lessons_all.count()
        elif tab == 'week':
            first_day = current_date - timedelta(days=current_date.weekday())
            last_day = first_day + timedelta(days=6)
            lessons_all = lessons.filter(day_of_week__gte=first_day, day_of_week__lte=last_day)
            numbers_lesson = lessons_all.count()
        elif tab == 'day':
            lessons_all = lessons.filter(day_of_week=current_date)
            numbers_lesson = lessons_all.count()


        grouped_lessons = []
        sorted_lessons = sorted(lessons_all, key=lambda x: x.start_time)
        unique_days = sorted(set(lesson.day_of_week for lesson in sorted_lessons))
        for day in unique_days:
            daily_lessons = [lesson for lesson in sorted_lessons if lesson.day_of_week == day]
            grouped_lessons.append((day, daily_lessons))
        print(sort)
        context = {
            'active': tab,
            'lessons': sorted_lessons,
            'numbers_lesson': numbers_lesson,
            'grouped_lessons': grouped_lessons,
            'sort': sort
        }
        return render(request, 'home_month.html', context)
