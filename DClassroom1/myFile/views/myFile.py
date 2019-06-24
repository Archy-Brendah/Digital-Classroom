from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,ListView,CreateView,UpdateView
from django.core.files.storage import FileSystemStorage
from ..forms import *
from ..models import *
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from PyPDF2 import PdfFileReader

from django.contrib import messages
from django.contrib.auth import login
from django.db import transaction
from django.db.models import Count
from django.utils.decorators import method_decorator
from ..decorators import student_required
from ..decorators import teacher_required
from ..decorators import superuser_required
from django.utils.safestring import mark_safe
import json






class Home(TemplateView):
	template_name='home.html'
class Home1(TemplateView):
	template_name='home1.html'
	


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'
class SuperuserSignUpView(CreateView):
    model = User
    form_class = SuperuserSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'super'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile')


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('profile')
        if request.user.is_student:
        	return redirect('profile')
        else:
            return redirect('profile')
    return render(request, 'home.html')



@login_required
@teacher_required
def  upload(request):
	context={}
	if request.method =='POST':

		uploaded_file=request.FILES['document']
		
		fs= FileSystemStorage()
		name=fs.save(uploaded_file.name,uploaded_file)
		

		context['url']= fs.url(name)
	return render(request,'upload.html',context)


def book_list(request):
	SearchE=request.POST.get("search")
	books = Book.objects.filter(lecturer=request.user)
	return render(request, 'book_list.html', {'books':books})
def student_book_list(request):
	SearchE=request.POST.get("search")
	bookys = Book.objects.all()
	return render(request, 'student_book_list.html', {'bookys':bookys})

@login_required
@teacher_required
def upload_book(request):
	# my_units = Unit.objects.filter(Instructor=user.request.username)
	if request.method =='POST':
		form = BookForm(request.POST, request.FILES, user=request.user)
		if form.is_valid():	
			fullform=form.save(commit=False)
			fullform.lecturer=request.user
			fullform.save()
			messages.success(request, 'documents upload successfully! ')
	else:
		form=BookForm(user=request.user)
		
	return render(request, 'upload_book.html', {
		'form':form,
		})
@login_required
@teacher_required
def delete_book(request,pk):
	if request.method=='POST':
		book=Book.objects.get(pk=pk)
		book.delete()
		messages.success(request, 'the document has been deleted ! ')
	return redirect('book_list')

# Create your views here.
class BookListView(ListView):
	model=Book
	template_name ='class_book_list.html'
	context_object_name = 'books'
class UploadBookView(CreateView):
	model=Book
	form_class=BookForm
	success_url=reverse_lazy('class_book_list')
	template_name='upload_book.html'

@login_required
@teacher_required
def Ylink(request):
	ylinks=YLinks.objects.all()
	if request.method=='POST':
	
		form=LinksForm(request.POST,user=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'The link has been sent! ')
			# return redirect('linklist')
	form=LinksForm(user=request.user)
	
	
	args={'form':form ,'ylinks':ylinks}		
	return render(request, 'mylinks.html',args)
def Ylink_list(request):
	ylinks=YLinks.objects.all()
	
	return render(request,'Ylink_list.html',{'ylinks':ylinks})
# @login_required
# @teacher_required
def Comm(request):
	# print(request.user)
	
	DateW =request.POST.get('date_away')
	comms=Comms.objects.filter(date=DateW)
	courses = Unit.objects.filter(Instructor=request.user)
	if request.method=='POST':
		course = request.POST.get('subject')
		title = request.POST.get('title')
		body = request.POST.get('body')
		print(course)
		print(title)
		print(body)
		com = Comms()
		com.subject= Course.objects.get(pk=course)
		com.Title = title
		com.Body = body
		com.lecturer=request.user
		com.save()

		# form=CommsForm(request.POST,user=request.user)
		# unit = request.POST.get('subject')
		# print(unit)
		# unit_instance = Unit.objects.get(Instructor=request.user)
		# form.subject =	unit_instance
		
		# fullform = form.save(commit=False)
		# # fullform.subject = unit_instance
		# fullform.lecturer=request.user
		# fullform.save()
		# print(unit)
		# print(unit_instance)
		messages.success(request, 'Message sent successfully! ')
			# return redirect('Commlist')
	# else:
	# 	form=CommsForm(user=request.user)

		# args={}

	return render(request,'Comm.html',{'comms':comms, 'courses':courses})

@login_required
@student_required
def Comm_List(request):

	subjects=Course.objects.filter(interested_students__user=request.user)
	comms= Comms.objects.filter(subject__in=subjects)
	#comms=Subject.objects.filter(subject__=request.user)
   	# students = Comms.objects.all()
	# user = Comms.objects.values_list('lecturer')
	# print(comms)
	print(comms)

	return render(request,'CommList.html',{'comms':comms})


def delete_comm(request,pk):
	if request.method=='POST':
		comms=Comms.objects.get(pk=pk)
		comms.delete()
		# messages.success(request, 'the document has been deleted ! ')
	return redirect('Commlist')

def Comm_Search(request):
	DateW =request.POST.get('date_away')
	try:
		searchcomms=Comms.objects.filter(date=DateW)
		return render(request,'CommSearch.html',{'searchcomms':searchcomms})
	except Comms.DoesNotExist:
		return render(request,'registration/404.html')
	
@login_required
@teacher_required	
def Reply(request):
	replys=Replys.objects.all()
	if request.method=='POST':
		form=ReplyForm(request.POST)
		if form.is_valid():
			form.save()
			# return redirect('Replylist')
	else:
		form=ReplyForm()
	
	return render(request,'Reply.html',{'form':form,'replys':replys})
def Reply_List(request):
	replys=Replys.objects.all()
	return render(request,'ReplyList.html',{'replys':replys})
def  Upload_Comm(request):
	context={}
	if request.method =='POST':
		uploaded_file=request.FILES['document']
		fs= FileSystemStorage()
		name=fs.save(uploaded_file.name,uploaded_file)
		context['url']= fs.url(name)
	return render(request,'UploadComm.html',context)


def RegisterStudent(request):
	if request.method == 'POST':
		print(request.POST)
		form = RegisterStudentForm(request.POST)
		course = Course.objects.get(id=request.POST['course'])
		students = course.interested_students.all()

	else:	
		students = []
		form = RegisterStudentForm()
	return render(request,'courses/View_register_student.html',context={'students':students, 'form': form})



def RegisterCourse(request):
	if request.method=='POST':
		form=RegisterCourseForm(request.POST, user=request.user)
		print(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Message sent successfully! ')
			
	else:
		form=RegisterCourseForm(user=request.user)
	args={'form':form,}
	return render(request,'courses/RegisterCourse.html',args)
	

@login_required
@superuser_required
def unit(request):
	# units=Unit.objects.all()
	# units=Unit.objects.all()

	# print (units)
	if request.method=='POST':
		form=unitForm(request.POST)
		if form.is_valid():
			# new_subject = Subject()
			# new_subject.name= request.POST['Code']
			# new_subject.save()
			units = Unit.objects.filter(Instructor=request.POST['Instructor'])
			unit1 = 0.0
			for unit in units:
				unit1+=unit.course.CF

			course_cf = Course.objects.filter(id=request.POST['course'])[0]
			unit1+=course_cf.CF
			

			if unit1 < 10:
				form.save()
				messages.success(request, 'Message sent successfully! ')
			else:
				messages.warning(request, "lecturer already have enough units")
			# return redirect('unitlist')
	else:
		form=unitForm()
	args={'form':form,}
	return render(request,'courses/unit.html',args)

def load_course(request):
	Period_id = request.GET.get('Period')
	cities = Course.objects.filter(Period_id=Period_id).order_by('course_title')
	cities_list = list(cities)  
	return JsonResponse(cities_list, safe=False)
	# return render(request, 'courses/cozdropdownlist.html', {'cities': cities})


def load_cities(request):
	print('loading cities')
	Period_id = request.GET.get('Period')
	print(Period_id)
	cities = Course.objects.filter(Period_id=Period_id).order_by('course_title')
	return render(request,'courses/cdropdown_list.html', {'cities': cities})

import xlrd
def UploadFile(request,f):
	book = xlrd.open_workbook(file_contents=f.read())
	for sheet in book.sheets():
		number_of_rows = sheet.nrows
		number_of_columns = sheet.ncols
		for row in range(1, number_of_rows):
			course_code = (sheet.cell(row, 0).value)
			course_title = (sheet.cell(row, 1).value)
			l = (sheet.cell(row, 2).value)
			p = (sheet.cell(row, 3).value)
			t = (sheet.cell(row, 4).value)
			cf= (sheet.cell(row, 5).value)
			period = (sheet.cell(row, 6).value)
			course = Course()
			course.course_code = course_code
			course.course_title = course_title
			course.L = l
			course.P = p
			course.T = t
			course.CF = cf
			mytime=Period.objects.filter(Period_time=period)[0]
			course.Period = mytime
			# course.semester = sem
			course.save()

def MyUnit(request):
	if request.method =='POST':
		 UploadFile(request, request.FILES['courses'])
		 return redirect('unit')

	return render(request, 'courses/create_courses.html',{} )
def unit_List():
	
	y1s1=[]
	y1s2=[]
	y2s1=[]
	y2s2=[]
	y3s1=[]
	y3s2=[]
	y4s1=[]
	y4s2=[]
	units=Unit.objects.all()
	for unit in units:
		if unit.Period_id == 1:
		  y1s1.append(unit)
		  template='y1s1List.html'
		elif unit.Period_id==2:
			y1s2.append(unit)
			template='y1s2.List.html'
		elif unit.Period_id==3:
			y2s1.append(unit)
			template='y2s1List.html'
		elif unit.Period_id==4:
			y2s2.append(unit)
			template='y2s2List.html'
		elif unit.Period_id==5:
			y3s1.append(unit)
			template='y3s1List.html'
		elif unit.Period_id==6:
			y3s2.append(unit)
			template='y3s2List.html'
		elif unit.Period_id==7:
			y4s1.append(unit)
			template='y4s1List.html'
		else :
			y4s2.append(unit)
			template='y4s2List.'
	unitlist=[y1s1,y1s2,y2s1,y2s2,y3s1,y3s2,y4s1,y4s2]
	return (unitlist)

def unitlist(request):
	template='courses/unitList.html'
	return render(request,template)
def Year1sem1_List(request):
	units=Unit.objects.all()
	unitlist = unit_List()
	y1s1=[]
	if unitlist[0]:
		y1s1 = unitlist[0]
	else:
		pass

	return render(request,'courses/y1s1List.html',{'y1s1':y1s1})

def Year1sem2_List(request):
	units=Unit.objects.all()
	unitlist = unit_List()
	y1s2=[]
	if unitlist[1]:
		y1s2 = unitlist[1]
	else:
		pass

	return render(request,'courses/y1s2List.html',{'y1s2':y1s2})

def Year2sem1_List(request):
	units=Unit.objects.all()
	unitlist = unit_List()
	y2s1=[]
	
	if unitlist[2]:
		y2s1 = unitlist[2]
	else:
		pass

	return render(request,'courses/y2s1List.html',{'y2s1':y2s1})

def Year2sem2_List(request):
	units=Unit.objects.all()
	unitlist = unit_List()
	y2s2=[]
	if unitlist[3]:
		y2s2 = unitlist[3]
	else:
		pass

	return render(request,'courses/y2s2List.html',{'y2s2':y2s2})

def Year3sem1_List(request):
	units=Unit.objects.all()
	unitlist = unit_List()
	y3s1=[]
	if unitlist[4]:
		y3s1 = unitlist[4]
	else:
		pass
	
	return render(request,'courses/y3s1List.html',{'y3s1':y3s1})

def Year3sem2_List(request):

	units=Unit.objects.all()
	unitlist = unit_List()
	y3s2=[]
	if unitlist[5]:
		y3s2 = unitlist[5]
	else:
		pass
	return render(request,'courses/y3s2List.html',{'y3s2':y3s2})

def Year4sem1_List(request):
	units=Unit.objects.all()
	unitlist = unit_List()
	y4s1=[]
	if unitlist[6]:
		y4s1 = unitlist[6]
	else:
		pass
	
	return render(request,'courses/y4s1List.html',{'y4s1':y4s1})
# 
def Year4sem2_List(request):
	units=Unit.objects.all()
	unitlist = unit_List()
	y4s2=[]
	if unitlist[7]:
		y4s2 = unitlist[7]
	else:
		pass
	
	return render(request,'courses/y4s2List.html',{'y4s2':y4s2})

def view_message(request, id):
	message = Comms.objects.get(id=id)
	return render(request, 'view_message.html', {'message':message})

def my_message(request):
	
	mess=Message.objects.all()
	if request.method=='POST':
		form=MessForm(request.POST)
		if form.is_valid():
			form = form.save()
		
			messages.success(request, 'Message sent successfully! ')
	else:
		form=MessForm()

		# args={}

	return render(request,'students/Message.html',{'form':form,'mess':mess})
def Message_List(request):
	mess=Message.objects.all()
	print(mess)
	
	return render(request,'students/MessageList.html',{'mess':mess})

def view_mess(request, id):
	mess = Message.objects.get(id=id)
	return render(request, 'students/view_mess.html', {'mess':mess})



def profile(request):
	return render(request,'profile.html')

	











# chat
def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })