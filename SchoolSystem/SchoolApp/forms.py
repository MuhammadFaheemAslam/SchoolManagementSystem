from django import forms 
from .models import Student


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 
            'last_name', 
            'father_name',  
            'date_of_birth', 
            'b_form_cnic', 
            'gender', 
            'father_cnic', 
            'address',  
            'phone_number', 
            'email',
            'profile_pic'
            # 'status',  
            # 'age',  # Exclude age as it is auto-calculated
            # 'st_class',  # Uncomment this if it exists in the model
        ]

    # Override the date_of_birth field to use a date picker
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',  # This allows for a date picker in modern browsers
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD'  # Placeholder for better UX
        })
    )

    # Define widgets for each field
    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'father_name': forms.TextInput(attrs={'class': 'form-control'}),
        'b_form_cnic': forms.TextInput(attrs={'class': 'form-control'}),
        'gender': forms.Select(attrs={'class': 'form-control'}),
        'address': forms.Textarea(attrs={'class': 'form-control'}),
        'father_cnic': forms.TextInput(attrs={'class': 'form-control'}),
        'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'status': forms.Select(attrs={'class': 'form-control'}),
        # 'age': forms.NumberInput(attrs={'class': 'form-control'}),  # Not necessary to include in the form
        # 'st_class': forms.Select(attrs={'class': 'form-control'}),  # Uncomment this if it exists in the model
    }
