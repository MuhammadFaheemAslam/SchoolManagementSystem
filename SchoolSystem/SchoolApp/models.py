import datetime
from django.db.models import Max
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import uuid  # For generating unique roll numbers
from django.db import models
from django.core.validators import MaxValueValidator, EmailValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Customuser(AbstractUser):
    USER = (
        (1,'HOD'),
        (2,'STAFF'),
        (3, 'STUDENT')
    )

    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    
    date_of_birth = models.DateField()
    b_form_cnic = models.CharField(max_length=13, unique=True)
    rollnumber = models.PositiveIntegerField(unique=True, blank=True)  # Auto-generated roll number
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(max_length=100)
    father_cnic = models.CharField(max_length=13)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(validators=[EmailValidator()], blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100)], editable=False)
    enrollment_date = models.DateField(default=timezone.now)
    profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True)
    religion = models.CharField(max_length=10, blank=True)
    registration_number = models.CharField(max_length=20, unique=True, blank=True)  # Auto-generated registration number
    classs = models.CharField(max_length=20)
    
    def calculate_age(self):
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = datetime.datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
        today = datetime.date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def save(self, *args, **kwargs):
        self.age = self.calculate_age()
        super(Student, self).save(*args, **kwargs)

        # Auto-generate registration number if not set
        if not self.registration_number:
            current_year = datetime.datetime.now().year
            last_student = Student.objects.filter(registration_number__startswith=f"REG{current_year}").order_by('-id').first()
            
            if last_student:
                last_reg_number = int(last_student.registration_number.split('-')[-1])
                new_reg_number = last_reg_number + 1
            else:
                new_reg_number = 1
                
            self.registration_number = f"REG{current_year}-{new_reg_number:03d}"
        
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Signal to auto-generate roll number before saving the student
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Student)
def set_rollnumber(sender, instance, **kwargs):
    if not instance.rollnumber:
        # Auto-generate roll number by incrementing the highest existing one
        last_roll_number = Student.objects.all().aggregate(Max('rollnumber'))['rollnumber__max']
        if last_roll_number:
            instance.rollnumber = last_roll_number + 1
        else:
            instance.rollnumber = 1




class Courses(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    credit_hours = models.PositiveIntegerField()

    def __str__(self):
        return self.course_name
