from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

from django.core.validators import RegexValidator


# user=models.ForeignKey('auth.User',on_delete=models.CASCADE)


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # first_name = models.CharField(max_length=100, unique=True, blank=False)
    # validators = [RegexValidator('^[S][P]{0,1}[1][3]/[0-9]{5,6}/[0-9]{2}$' or '^[C][', 'Invalid registration number.')])

    def __str__(self):
        return str(self.username)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')
    objects = models.Manager()

    def __str__(self):
        return str(self.name)

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-success" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Teacherid(models.Model):
    Empid = models.CharField(max_length=100)


class Period(models.Model):
    Period_time = models.CharField(max_length=20)

    def __str__(self):
        return str(self.Period_time)


# Create your models here.
# Create your models here.s
class Course(models.Model):
    course_code = models.CharField(max_length=100)
    course_title = models.CharField(max_length=100)
    L = models.PositiveIntegerField()
    P = models.PositiveIntegerField()
    T = models.PositiveIntegerField()
    CF = models.FloatField()
    Period = models.ForeignKey(Period, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return str(self.course_code)


class Unit(models.Model):
    Period = models.ForeignKey(Period, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return str(self.course)


class Book(models.Model):
    Unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # Period=models.ForeignKey(Period,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='books/pdfs/')
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)


class YLinks(models.Model):
    Unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    # Period=models.ForeignKey('myFile.Course',on_delete=models.CASCADE)
    mylink = models.URLField(max_length=200)
    title = models.CharField(max_length=100, default='comp333')


class Message(models.Model):
    Party = models.ForeignKey(User, on_delete=models.CASCADE, related_name="party")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    Title = models.CharField(max_length=100)
    Content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        ordering = ('-date',)


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class Comms(models.Model):
    subject = models.ForeignKey(Course, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Body = models.TextField()
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    # Letter=models.FileField(upload_to='books/letters/')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.subject)


class Replys(models.Model):
    Content = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)

    msg = models.ForeignKey(Message, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    interests = models.ManyToManyField(Course, null=True, blank=True, related_name='interested_students')

    def get_unanswered_questions(self, quiz):
        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
        return questions

    def __str__(self):
        return str(self.user.username)


class TakenQuiz(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')
