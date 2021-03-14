from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Course(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    img = models.ImageField(default='default.jpg', upload_to='course_images')
    free = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})


class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    number = models.IntegerField()
    video_url = models.CharField(max_length=100)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson-detail', kwargs={'slug': self.course.slug, 'lesson_slug': self.slug})


class Comment(models.Model):
    lesson_comment = models.ForeignKey(Lesson, verbose_name='Коментарий к уроку', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE)
    text_comment = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return 'Комментарий от {} к {}'.format(self.author, self.lesson_comment)