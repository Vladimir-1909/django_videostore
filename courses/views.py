from django.shortcuts import render, reverse
from .models import Course, Lesson, Comment
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)
from django.views.generic.edit import FormMixin
from .forms import CreateCourseForm, CommentForm
from cloudipsp import Api, Checkout
import json
import time


class HomePage(ListView):
    model = Course
    template_name = 'courses/home.html'
    context_object_name = 'courses'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePage, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница сайта'
        return ctx



def tarrifsPage(request):
    api = Api(merchant_id=1466082,
              secret_key='3Wd3oFiT91v2MExU3sIxmPwb3K7DRSsi')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": 100000,
        "order_desc": "Покупка подписки на сайте Shopster",
        "order_id": str(time.time()),
        "merchant_data": "exemple@mail.com"
    }
    url = checkout.url(data).get('checkout_url')
    return render(request, 'courses/tarrifs.html', {'title': 'Тарифы на сайте', 'url': url})


def callback_payment(request):
    if request.method == 'POST':
        data = json.load(request.POST)

        # print(data) # email - оплатившего


class CourseDetailPage(DetailView):
    model = Course
    template_name = 'courses/course-detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CourseDetailPage, self).get_context_data(**kwargs)
        ctx['title'] = Course.objects.filter(slug=self.kwargs['slug']).first()
        ctx['lessons'] = Lesson.objects.filter(course=ctx['title']).order_by('number')
        # print(ctx['lessons'].query)
        return ctx


class LessonDetailPage(FormMixin, DetailView):
    model = Course
    template_name = 'courses/lessons-detail.html'
    form_class = CommentForm
    object = Comment

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LessonDetailPage, self).get_context_data(**kwargs)
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        lesson = list(Lesson.objects.filter(course=course).filter(slug=self.kwargs['lesson_slug']).values())
        lesson_id = Lesson.objects.filter(slug=self.kwargs['lesson_slug']).first()
        comments = Comment.objects.filter(lesson_comment=lesson_id).order_by('-id')
        ctx['title'] = lesson[0]['title']
        ctx['desc'] = lesson[0]['description']
        ctx['video'] = lesson[0]['video_url'].split('=')[1]
        ctx['commForm'] = CommentForm()
        ctx['comments'] = comments
        # print(comments.query)
        return ctx

    def get_success_url(self):
        return reverse('lesson-detail', kwargs={'slug': self.kwargs['slug'], 'lesson_slug': self.kwargs['lesson_slug']})


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        lesson = Lesson.objects.filter(course=course).filter(slug=self.kwargs['lesson_slug']).first()

        self.object = form.save(commit=False)
        self.object.lesson_comment = lesson
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class CreateCourse(CreateView):
    model = Course
    template_name = 'courses/create_course.html'
    form_class = CreateCourseForm

    def get_context_data(self, **kwards):
        ctx = super(CreateCourse, self).get_context_data(**kwards)
        ctx['title'] = 'Добавление нового курса'
        ctx['btn_text'] = 'Добавить курс'
        return ctx

