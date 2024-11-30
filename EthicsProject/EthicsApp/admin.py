
from django.contrib import admin
from .views.models import *

# Register your models here.
admin.site.register(Accounts)
admin.site.register(Student)
admin.site.register(Appointments)
admin.site.register(Account_Type)
admin.site.register(Comments)
admin.site.register(Notification)
admin.site.register(Schedule)
admin.site.register(Manuscripts)
admin.site.register(College)
admin.site.register(Reviewer)
admin.site.register(Category)
admin.site.register(TypeOfStudy)
admin.site.register(BasicRequirements)
admin.site.register(SupplementaryRequirements)
admin.site.register(EthicalRiskQuestions)
admin.site.register(EthicalRiskAnswers)
admin.site.register(ThesisType)

