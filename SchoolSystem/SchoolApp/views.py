from django.shortcuts import render
from .models import Student

# Create your views here.
def viewStudents(request):
    return render(request, 'student/index.html', {
    'students': Student.objects.all()
  })
