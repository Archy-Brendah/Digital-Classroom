"""DClassroom1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
# from myFile import views 
from django.conf import settings
from django.conf.urls.static import static
from myFile.views import myFile, students, teachers


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('home',views.home1,name='home1'),
    # path('signup/',views.signup,name='signup'),
     path('', include('myFile.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/',myFile.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),

    path('accounts/signup/superuser/', myFile.SuperuserSignUpView.as_view(), name='superuser_signup'),
    
    # path('regno/',students.enterReg, name='regno'),
    # path('regno/regSuccess',students.StudentRegno, name='regSuccess'),
 
    
    

    path('',myFile.Home.as_view(),name='home'),
    path('home',myFile.Home1.as_view(),name='home1'),
    path('about/',myFile.About.as_view(),name='about'),
    path('contact/',myFile.Contact.as_view(),name='contact'),

    path('upload/', myFile.upload,name='upload'),
    path('books/', myFile.book_list, name='book_list'),
     path('books/student', myFile.student_book_list, name='student_book_list'),
    

    path('books/upload', myFile.upload_book, name='upload_book'),
    path('books/<int:pk>/', myFile.delete_book, name='delete_book'),
    path('link/', myFile.Ylink, name='link'),
    path('link/linklist',myFile.Ylink_list,name='linklist'),
    path('Comm',myFile.Comm,name='Comm'),
    path('Comm/Commlist',myFile.Comm_List,name='Commlist'),
    path('Comm/<int:pk>/', myFile.delete_comm, name='delete_comm'),
    path('Comm/Commsearch',myFile.Comm_Search,name='Commsearch'),
    path('Comm/view/<int:id>/', myFile.view_message, name='view_message'),
    path('Message',myFile.my_message,name='Message'),
    path('Message/MessageList',myFile.Message_List,name='MessageList'),
    path('Message/view/<title>/',myFile.view_mess,name='view_mess'),
   
    path('Reply',myFile.Reply,name='Reply'),
    path('Reply/Replylist',myFile.Reply_List,name='Replylist'),
    path('uploadComm/',myFile.Upload_Comm,name='Upload_Comm'),

    

    path('class/books', myFile.BookListView.as_view(), name='class_book_list'),
    path('class/books/upload', myFile.UploadBookView.as_view(), name='class_upload_book'),

    
    
    path('unit/',myFile.unit,name='unit'),
    path('unitlisty/',myFile.unit_List,name='unitlisty'),
    path('unitlist/',myFile.unitlist,name='unitlist'),
    path('unit/registercourse/',myFile.RegisterCourse,name='registercourse'),
    path('registerStudent/',myFile.RegisterStudent,name='register_student'),


    path('ajax/load-cities/', myFile.load_cities, name='ajax_load_cities'),
    path('ajax/load-course/', myFile.load_course, name='ajax_load_course'),
   
   
    
    path('unitlist/y1s1list',myFile.Year1sem1_List,name='y1s1list'),
    path('unitlist/y1s2list',myFile.Year1sem2_List,name='y1s2list'),
    path('unitlist/y2s1list',myFile.Year2sem1_List,name='y2s1list'),
    path('unitlist/y2s2list',myFile.Year2sem2_List,name='y2s2list'),
    path('unitlist/y3s1list',myFile.Year3sem1_List,name='y3s1list'),
    path('unitlist/y3s2list',myFile.Year3sem2_List,name='y3s2list'),
    path('unitlist/y4s1list',myFile.Year4sem1_List,name='y4s1list'),
    path('unitlist/y4s2list',myFile.Year4sem2_List,name='y4s2list'),
    path('profile/',myFile.profile,name='profile'),
    path('add/units/', myFile.MyUnit, name='create_units'),

    # path('chat/',myFile.index,name='index'),
    # re_path(r'^(?P<room_name>[^/]+)/$', myFile.room, name='room'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
