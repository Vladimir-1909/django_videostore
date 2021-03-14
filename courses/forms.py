from django import forms
from django.forms import Textarea
from .models import Course, Comment


class CreateCourseForm(forms.ModelForm):
    slug = forms.CharField(
        label='Название URL',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Название URL'
        })
    )
    title = forms.CharField(
        label='Название курса',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название курса'
        })
    )
    description = forms.CharField(
        label='Описание курса',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите Описание курса'
        })
    )
    img = forms.ImageField(label='Изображение курса', required=False)

    class Meta:
        model = Course
        fields = ['slug', 'title', 'description', 'img']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields['text_comment'].widget = Textarea(attrs={'rows': 5, 'class': 'form-control'})