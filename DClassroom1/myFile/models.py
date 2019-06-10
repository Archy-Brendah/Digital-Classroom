from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe
from django.utils import timezone

# user=models.ForeignKey('auth.User',on_delete=models.CASCADE)



class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    def __str__(self):
    	return self.username

   


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
	user=models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
	
	def __str__(self):
		return self.user.username
		
class Studentrg(models.Model):
    
    
    interests = models.ManyToManyField(Subject, related_name='interested_student')
    
class Teacherid(models.Model):
    
    Empid=models.CharField(max_length=100)
   




# Create your models here.
# Create your models here.s





class Period(models.Model):
	Year_semester=(
		('y1s1','year1semester1'),
		('y1s2','year1semester2'),
		('y2s1','year2semester1'),
		('y2s2','year2semester2'),
		('y3s1','year3semester1'),
		('y3s2','year3semester2'),
		('y4s1','year4semester1'),
		('y4s2','year4semester2')
		)
	# name=models.CharField(max_length=100)

	Year_semester=models.CharField(max_length=4,choices=Year_semester, unique=True)
	# 

	def __str__(self):
		return self.Year_semester



class Unit(models.Model):
	Period=models.ForeignKey(Period,on_delete=models.CASCADE)
	Code=models.CharField(max_length=100)
	Title=models.CharField(max_length=100)
	Instructor=models.CharField(max_length=100)
	Cf=models.CharField(max_length=100)
	def __str__(self):
		return self.Title



class Book(models.Model):
	
	Unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
	Period=models.ForeignKey(Period,on_delete=models.CASCADE)
	title= models.CharField(max_length=100)
	author=models.CharField(max_length=100)
	pdf=models.FileField(upload_to='books/pdfs/')
	cover = models.ImageField(upload_to='books/covers/',null=True, blank=True)
	lecturer=models.ForeignKey(User, on_delete=models.CASCADE)

	def delete(self,*args,**kwargs):
		self.pdf.delete()
		self.cover.delete()
		super().delete(*args,**kwargs)
	
class YLinks(models.Model):
	
	Unit=models.ForeignKey(Unit,on_delete=models.CASCADE)
	Period=models.ForeignKey(Period,on_delete=models.CASCADE)
	mylink=models.URLField(max_length=200)
	title=models.CharField(max_length=100, default='comp333')
class Message(models.Model):
	Party=models.CharField(max_length=100)
	Title=models.CharField(max_length=100)
	Content=models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	objects = models.Manager()





	

		
class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')

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
	subject=models.ForeignKey(Subject,on_delete=models.CASCADE)	
	Title=models.CharField(max_length=100)
	Body=models.TextField()
	lecturer=models.ForeignKey(User, on_delete=models.CASCADE)
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
    interests = models.ManyToManyField(Subject, related_name='interested_students')

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
