from django import forms
from .models import Student, Manuscripts, Appointments, Accounts

class StudentProfileForm(forms.ModelForm):
    # Add fields from the auth_user model
    username = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    email = forms.EmailField(
        max_length=255, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # Fields from the Student model
    smc_student_no = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    mobile_number = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Include manuscript title and other manuscript details
    manuscript_title = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), 
        required=False
    )
    manuscript_category = forms.CharField(
        max_length=350, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), 
        required=False
    )
    manuscript_type_of_study = forms.CharField(
        max_length=350, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), 
        required=False
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'smc_student_no', 'mobile_number', 
                  'manuscript_title', 'manuscript_category', 'manuscript_type_of_study']
        widgets = {
            'smc_student_no': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Pop out the 'user' and 'student' from kwargs
        user = kwargs.pop('user', None)  # Get the user instance
        student = kwargs.pop('student', None)  # Get the student instance
        super().__init__(*args, **kwargs)
        
        # Initialize the auth_user fields from the user instance
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name  # Fetch last name from User

        # Initialize student-related fields
        if student:
            self.fields['smc_student_no'].initial = student.smc_student_no
            self.fields['mobile_number'].initial = student.mobile_number

            # Fetch manuscript details from the Manuscripts model
            if student.manuscript_id:
                manuscript = student.manuscript_id
                self.fields['manuscript_title'].initial = manuscript.thesis_title
                self.fields['manuscript_category'].initial = manuscript.category_name.category_name  # Assuming Category model
                self.fields['manuscript_type_of_study'].initial = manuscript.type_of_study.type_of_study  # Assuming TypeOfStudy model
