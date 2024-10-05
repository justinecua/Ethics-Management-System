from django.db import models
from django.conf import settings

class Student(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE) 
    smc_student_no = models.CharField(max_length =255)
    mobile_number = models.CharField(max_length =255)
    receipt_no = models.CharField(max_length =255)

    def __str__(self):
        return f"{self.auth_user}"

class Apointments(models.Model):
    appointment_date = models.DateField(null=True)
    appointment_name = models.CharField(max_length =255)
    status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
 
    def __str__(self):
        return f"{self.appointment_date} {self.appointment_name}"

class Reviewer(models.Model):
    first_name = models.CharField(max_length =255) 
    last_name = models.CharField(max_length =255) 
    smc_email = models.EmailField(max_length =255)
    smc_id_no = models.CharField(max_length =255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} "

class College(models.Model):
    college_name = models.CharField(max_length =255)
    college_initials = models.CharField(max_length =255)

    def __str__(self):
        return f"{self.college_name} {self.college_initials} "

class Account_Type(models.Model):
    Account_type = models.CharField(max_length =255)
    
    def __str__(self):
        return f"{self.Account_type}"

class Accounts(models.Model):
    student_id= models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    reviewer_id= models.ForeignKey(Reviewer, on_delete=models.CASCADE, null=True)
    college_id= models.ForeignKey(College, on_delete=models.CASCADE, null=True)
    account_typeid= models.ForeignKey(Account_Type, on_delete=models.CASCADE, null=True)
   
    def __str__(self):
        return f"{self.student_id}"

class Manuscripts(models.Model):
     thesis_title = models.CharField(max_length =255)
     thesis_description = models.TextField(null=True)
     category_name = models.CharField(max_length =255)
     type_of_study = models.CharField(max_length =700)
     study_site = models.CharField(max_length =255)
     no_studyparticipants= models.CharField(max_length =255)
     file = models.URLField(verbose_name="File Url")
     account_id= models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    
     def __str__(self):
        return f"{self.thesis_title} {self.thesis_description}"


class Schedule(models.Model):
    schedname = models.CharField(max_length=120, default="Unnamed Schedule")
    datetime = models.DateTimeField(null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f"{self.schedname} on {self.datetime}"

class Notification(models.Model):
    date = models.DateField(null=True)
    status = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
 
    def __str__(self):
        return f"{self.date} {self. status} {self.name}"
    
class Comments(models.Model):
    commend = models.CharField(max_length=100)
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.date} {self. comment}"
