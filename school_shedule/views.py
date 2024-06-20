import calendar
from datetime import datetime, timedelta

from django.shortcuts import render
from django.views import View

from school_shedule.models import Lesson


class HomeMonth(View):
    def get(self, request):
        tab = request.GET.get('tab', 'day')
        return self.render_schedule(request, tab)

    def post(self, request, *args, **kwargs):
        tab = request.GET.get('tab', 'day')  # Отримати активне значення tab
        return self.render_schedule(request, tab)

    def render_schedule(self, request, tab):
        sort = ''
        if 'class_name' in request.POST:
            request.session['class'] = request.POST.get('class_name')
        if 'teacher_name' in request.POST:
            request.session['teacher'] = request.POST.get('teacher_name')
            sort = 'teacher'
        # отримуємо з сесії значення полів які відповідають за вчителя та клас
        class_name = request.session.get('class', '')
        teacher_name = request.session.get('teacher', '')

        numbers_lesson = ''
        lessons = Lesson.objects.all()
        # якщо сесія не порожня, товідбувається фільтрація з цими ж даними
        if class_name:
            lessons = lessons.filter(class_name=class_name)
            numbers_lesson = lessons.count()
        if teacher_name:
            lessons = lessons.filter(teacher=teacher_name)
            sort = 'teacher'
            numbers_lesson = lessons.count()
        current_date = datetime.now()

        # Фільтрування уроків якщо сесія class_name та teacher_name порожня та залежно від вибраного (місяць, день, тиждень)
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
        return render(request, 'home.html', context)


class ScheduleView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        print(start_date, end_date)
        return render(request, 'index.html')
