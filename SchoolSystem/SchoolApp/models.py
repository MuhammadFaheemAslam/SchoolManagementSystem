from datetime import date
from django.db import models
from django.core.validators import MaxValueValidator

import uuid  # For generating unique roll numbers
from django.db import models
from django.core.validators import MaxValueValidator, EmailValidator

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

    # New Course/Class Choices
    CLASS_CHOICES = [
        ('1st Grade', '1st Grade'),
        ('2nd Grade', '2nd Grade'),
        ('3rd Grade', '3rd Grade'),
        ('4th Grade', '4th Grade'),
        ('5th Grade', '5th Grade'),
        ('6th Grade', '6th Grade'),
        ('7th Grade', '7th Grade'),
        ('8th Grade', '8th Grade'),
        ('9th Grade', '9th Grade'),
        ('10th Grade', '10th Grade'),
        ('11th Grade', '11th Grade'),
        ('12th Grade', '12th Grade'),
        # Add more courses or classes as needed
    ]

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)  # Optional field
    last_name = models.CharField(max_length=50)
    
    date_of_birth = models.DateField()
    b_form_cnic = models.CharField(max_length=13, unique=True)  # New field for B-Form/CNIC
    rollnumber = models.CharField(max_length=20, unique=True, editable=False)  # Auto-generated
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(max_length=100)
    father_cnic = models.CharField(max_length=13, unique=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(validators=[EmailValidator()], blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    age = models.PositiveIntegerField(validators=[MaxValueValidator(100)], editable=False)  # Make age non-editable
    st_class = models.CharField(max_length=20, choices=CLASS_CHOICES)

    def save(self, *args, **kwargs):
        if not self.rollnumber:
            self.rollnumber = str(uuid.uuid4())[:8]  # Generate unique roll number (first 8 chars)
        
        # Calculate age based on date_of_birth
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
