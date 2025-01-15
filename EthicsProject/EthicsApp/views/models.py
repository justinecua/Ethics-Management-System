from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class Category(models.Model):
    category_name= models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"{self.category_name}"

class TypeOfStudy(models.Model):
    type_of_study = models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"{self.type_of_study}"

class Manuscripts(models.Model):
    thesis_title = models.CharField(max_length=255, null=True)
    thesis_description = models.TextField(max_length=800, null=True)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    type_of_study = models.ForeignKey(TypeOfStudy, on_delete=models.CASCADE, null=True)
    study_site = models.CharField(max_length=400, null=True)
    file = models.FileField(upload_to='manuscripts/', storage=FileSystemStorage())

    def __str__(self):
        return f"{self.thesis_title} - {self.thesis_description}"

class Student(models.Model):
    auth_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    smc_student_no = models.CharField(null=True, max_length =255)
    mobile_number = models.CharField(null=True, max_length =255)
    receipt_no = models.CharField(null=True, max_length =255)
    receipt_no2 = models.CharField(null=True, max_length=255)
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
    account_id = models.ForeignKey(Account_Type, on_delete=models.CASCADE, null=True)
    schedule_type = models.CharField(max_length=255, null=True)
    schedule_date = models.DateField(null=True)
    schedule_start_time = models.TimeField(null=True)
    schedule_end_time = models.TimeField(null=True)
    slot = models.CharField(max_length=25, null=True)

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
        return f"{self.ethicalQuestions}"

class ThesisType(models.Model):
    ThesisType = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.ThesisType}"

class Appointments(models.Model):
    appointment_date = models.DateField(null=True)
    appointment_name = models.CharField(max_length =255, null=True)
    duration_start_time = models.DateField(null=True)
    duration_end_time = models.DateField(null=True)
    status = models.CharField(max_length=100, null=True)
    transaction_id = models.CharField(max_length=100, null=True)
    institution = models.CharField(max_length=100, null=True)
    address_of_institution = models.CharField(max_length=100, null=True)
    basicRequirements_id = models.ForeignKey(BasicRequirements, on_delete=models.CASCADE, null=True)
    supplementaryRequirements_id = models.ForeignKey(SupplementaryRequirements, on_delete=models.CASCADE, null=True)
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    thesis_type_id = models.ForeignKey(ThesisType, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.appointment_date} {self.appointment_name}"


class EthicalRiskAnswers(models.Model):
    ethicalQuestions = models.ForeignKey(EthicalRiskQuestions, on_delete=models.CASCADE, null=True)
    ethicalAnswers = models.CharField(max_length=350, null=True)
    appointment_id = models.ForeignKey(Appointments, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.ethicalAnswers} {self.ethicalQuestions} {self.appointment_id}"


