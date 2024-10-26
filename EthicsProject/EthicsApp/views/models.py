from django.db import models
from django.conf import settings


class Manuscripts(models.Model):
     thesis_title = models.CharField(max_length =255, null=True)
     thesis_description = models.TextField(max_length=800, null=True)
     category_name_id = models.CharField(max_length =20, null=True)
     type_of_study_id = models.CharField(max_length =20, null=True)
     study_site = models.CharField(max_length =400, null=True)
     no_studyparticipants= models.CharField(max_length =255, null=True)
     file = models.URLField(verbose_name="File Url")

     def __str__(self):
        return f"{self.thesis_title} {self.thesis_description}"


class Student(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    smc_student_no = models.CharField(max_length =255)
    mobile_number = models.CharField(max_length =255)
    receipt_no = models.CharField(max_length =255)
    manuscript_id = models.ForeignKey(Manuscripts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.auth_user}"

class Reviewer(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    smc_id_no = models.CharField(max_length=255, null=True)
    manuscript_id = models.ForeignKey(Manuscripts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.auth_user}"

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
    invite_status= models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.account_typeid}"

class Schedule(models.Model):
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    schedule_type = models.CharField(max_length=255, null=True)
    schedule_date = models.DateField(null=True)
    schedule_start_time = models.TimeField(null=True)
    schedule_end_time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.account_id} Schedule on {self.schedule_date} from {self.schedule_start_time} to {self.schedule_end_time} ({self.schedule_type})"

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

class Category(models.Model):
    category_name= models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"{self.category_name}"

class TypeOfStudy(models.Model):
    type_of_study = models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"{self.type_of_study}"


class BasicRequirements(models.Model):
    basicRequirements = models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"{self.basicRequirements}"

class SupplementaryRequirements(models.Model):
    supplementaryRequirements = models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"{self.supplementaryRequirements}"


class EthicalRiskQuestions(models.Model):
    ethicalQuestions = models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"{self.basicRequirements}"


class EthicalRiskAnswers(models.Model):
    ethicalQuestions = models.ForeignKey(EthicalRiskQuestions, on_delete=models.CASCADE, null=True)
    ethicalAnswers = models.CharField(max_length=350, null=True)
    student_id= models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.basicRequirements}"

class Appointments(models.Model):
    appointment_date = models.DateField(null=True)
    appointment_name = models.CharField(max_length =255, null=True)
    status = models.CharField(max_length=100, null=True)
    transaction_id = models.CharField(max_length=100, null=True)
    institution = models.CharField(max_length=100, null=True)
    ethicalAnswers_id = models.ForeignKey(EthicalRiskAnswers, on_delete=models.CASCADE, null=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.appointment_date} {self.appointment_name}"


