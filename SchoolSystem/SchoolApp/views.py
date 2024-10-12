from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import StudentRegistrationForm  
from  SchoolApp.EmailBackEnd import EmailBackEnd
from django.contrib.auth.decorators import login_required




def login_page(request):
    return render(request, 'login.html')

def dologin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')    
        print('password:',password,'  email',email)   
        user = EmailBackEnd.authenticate(request, username=email, password=password)  
        print('user:',user) 
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type =='1':
                messages.success(request, "You have been logged in to HOD.")
                return redirect('hod_home')
            elif user_type =='2':
                messages.success(request, "You have been logged in Staff.")
                return HttpResponse('Staff')
            elif user_type =='3':
                messages.success(request, "You have been logged in Student.")
                return HttpResponse('Teacher')
            else:     
                messages.error(request, "Invalid email or password. Please try again.")
                return redirect('login_page')  # Redirect to your desired page after login
        else:
            messages.error(request, "Invalid email or password. Please try again.")
            return redirect('login_page')  # Redirect back to the login page on failure
    # else:
    #     return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out...."))
    return redirect('login_page')

@login_required(login_url='/')
def hod(request):
    return render(request, 'hod/home.html')

@login_required(login_url='/')
def base(request):
    return render(request, 'base.html')

# List all students
@login_required(login_url='/')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student/student_list.html', {'students': students})

# View details of a single student
@login_required(login_url='/')
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    print(student.id)
    return render(request, 'student/student_detail.html', {'student': student})


# Create a new student
@login_required(login_url='/')
def add_student(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        fathertname = request.POST.get('father_name')
        bform = request.POST.get('b_form')
        gender = request.POST.get('gender')
        dateofbirth = request.POST.get('date_of_birth')
        Cclass = request.POST.get('classes')
        religion = request.POST.get('religion')
        studentImage = request.POST.get('image')
        email = request.POST.get('email')
        fatherMobile = request.POST.get('phone_no')
        fatherCnic = request.POST.get('f_cnic')
        Address = request.POST.get('address')
        if Customuser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already Taken')
            return redirect('add_student')
        else:
          student = Student(
              first_name = firstname,
              last_name = lastname,
              father_name = fathertname,
              date_of_birth = dateofbirth,
              b_form_cnic = bform,
              gender = gender,
              address = Address,
              father_cnic = fatherCnic,
              phone_number = fatherMobile,
              email = email,
              profile_pic = studentImage,
              classs = Cclass,
              religion = religion
          )
          student.save()
          messages.success(request, 'Student Successfully saved')
          return redirect('student_list')
        
    return render(request, 'student/add_student.html')

# Update an existing student
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_detail', pk=student.pk)  # Redirect to student detail
    else:
        form = StudentRegistrationForm(instance=student)
    return render(request, 'student/student_form.html', {'form': form})

# Delete a student
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')  # Redirect to the student list after deletion
    return render(request, 'student/student_confirm_delete.html', {'student': student})
