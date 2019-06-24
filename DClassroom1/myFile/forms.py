from django import forms
from django.forms import TextInput
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms.widgets import CheckboxSelectMultiple


class TeacherSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''

    class Meta(UserCreationForm.Meta):
        model = User
        fields= ('username','first_name','last_name','email','password1', 'password2',)
        labels = {
        "first_name": "EmpId",
        "last_name":"Full_name"
    }
        
    
       
	
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

class SuperuserSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''

    class Meta(UserCreationForm.Meta):
        model = User
        fields= ('username','first_name','last_name','email','password1', 'password2',)
        labels = {
        "first_name": "EmpId",
        "last_name":"Full_name"
    }
        
       

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = True
        if commit:
            user.save()
        return user

class RegisterCourseForm(forms.ModelForm):
    Period = forms.ModelChoiceField(
        queryset=Period.objects.all(),
        empty_label=None,
        )

    interests = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model= Student
        fields=('Period', 'interests',)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RegisterCourseForm, self).__init__(*args, **kwargs)

        # self.fields['interests'].queryset = Course.objects.none()


        if 'Period' in self.data:
            print('data from ajax'+str(self.data))
            try:
                Period_id = int(self.data.get('Period'))
                self.fields['interests'].queryset = Course.objects.filter(Period_id=Period_id).order_by('course_title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['interests'].queryset = self.instance.Period.course_set.order_by('course_title')
        else:
            print("imeingia")


    def save(self):
        student = Student.objects.filter(user=self.user)[0]
        student.interests.add(*self.cleaned_data.get('interests'))
        student.save()
        return student

        
    

class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    # def __init__(self, *args, **kwargs):
    #     super(UserCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['password1'].help_text = ''
        

            

    class Meta(UserCreationForm.Meta):
        model = User
        fields= ('username','first_name','last_name','email','password1', 'password2',)
       
        labels = {
        "first_name": "RegNumber",
        "last_name":"Full_name"
    }
    

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        return user



class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

            
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class BookForm(forms.ModelForm):
    Unit = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
        )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['Unit'].queryset =Unit.objects.filter(Instructor=user)
    class Meta:
        model=Book
        # fields=('Period','Unit','title','author','pdf','cover')
        fields=('Unit','title','author','pdf','cover')



class LinksForm(forms.ModelForm):
    Unit = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
        )
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user')
        super(LinksForm, self).__init__(*args, **kwargs)
        self.fields['Unit'].queryset =Unit.objects.filter(Instructor=user)
    class Meta:
        model=YLinks
        fields=('Unit','mylink','title')
        # i have used both widgets and crispy although i should have used one of them
        widgets={'mylink':forms.TextInput(attrs={'class':'form-control','placeholder':'paste the link','name':'link'})}
		
			
class CommsForm(forms.ModelForm):
    subject = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
        )
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user')
        super(CommsForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset =Unit.objects.filter(Instructor=user)
    class Meta:
        model=Comms
        fields=('subject','Title','Body')
class MessForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=('Party','Title','Content')



class ReplyForm(forms.ModelForm):
	class Meta:
		model=Replys
		fields=['Content']

    

class unitForm(forms.ModelForm):
    # period = forms.ChoiceField()
    Instructor = forms.ModelChoiceField(
        queryset=None,
        empty_label=None,
        )
   
        
    class Meta:
        model=Unit
        fields=('Period','course','Instructor', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.none()

        super(unitForm, self).__init__(*args, **kwargs)
        self.fields['Instructor'].queryset =User.objects.filter(is_teacher=True)

        if 'Period' in self.data:
            print('data from ajax'+str(self.data))
            try:
                Period_id = int(self.data.get('Period'))
                self.fields['course'].queryset = Course.objects.filter(Period_id=Period_id).order_by('course_title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.Period.course_set.order_by('course_title')
        else:
            print("imeingia")


class RegisterStudentForm(forms.ModelForm):
    class Meta:
        model=Unit
        fields=('Period','course')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.none()

        
        if 'Period' in self.data:
            print('data from ajax'+str(self.data))
            try:
                Period_id = int(self.data.get('Period'))
                self.fields['course'].queryset = Course.objects.filter(Period_id=Period_id).order_by('course_title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.Period.course_set.order_by('course_title')
        else:
            print("imeingia")

            	