from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.contrib import messages
from .models import Student, Accounts, Reviewer, Account_Type, College, Category, TypeOfStudy, BasicRequirements, SupplementaryRequirements, EthicalRiskQuestions, Appointments, Schedule, ClaimStabs
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

from .models import *

def get_google_profile_picture(user):
    social_account = user.socialaccount_set.filter(provider='google').first()
    if social_account:
        return social_account.extra_data.get('picture')
    return None

def adminDashboard(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'admin/adminDashboard.html', context)

def adminAccounts(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    students = Student.objects.filter(
        auth_user__isnull=False,
        auth_user__is_superuser=False
    ).prefetch_related(
        Prefetch(
            'accounts_set',
            queryset=Accounts.objects.filter(account_typeid__Account_type='Student').select_related('college_id')
        )
    )

    reviewers = Reviewer.objects.filter(
        auth_user__isnull=False,
        auth_user__is_superuser=False
    ).prefetch_related(
        Prefetch(
            'accounts_set',
            queryset=Accounts.objects.filter(account_typeid__Account_type='Reviewer').select_related('college_id')
        )
    )

    admins = Reviewer.objects.filter(
        auth_user__isnull=False,
        auth_user__is_superuser=True
    ).prefetch_related(
        Prefetch(
            'accounts_set',
            queryset=Accounts.objects.filter(account_typeid__Account_type='Admin').select_related('college_id')
        )
    )

    accountType = Account_Type.objects.exclude(Account_type='Student')


    for student in students:
        student.google_picture = get_google_profile_picture(student.auth_user)

    for reviewer in reviewers:
        reviewer.google_picture = get_google_profile_picture(reviewer.auth_user)

    for admin in admins:
        admin.google_picture = get_google_profile_picture(admin.auth_user)

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'students': students,
        'reviewers': reviewers,
        'admins': admins,
        'accountTypes': accountType,
    }
    return render(request, 'admin/adminAccounts.html', context)

def adminAppointments(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    appointments = Appointments.objects.all().select_related(
        'account_id', 
        'account_id__student_id',  
        'account_id__student_id__manuscript_id', 
        'account_id__college_id'  
    ).prefetch_related(
        'account_id__student_id__manuscript_id__student_set' 
    )

    return render(request, 'admin/adminAppointments.html', {
        'appointments': appointments,
        'profile_picture': profile_picture,
        'account_type': account_type,

    })


from django.db.models import Max

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Reviewer, Manuscripts, Appointments

def assign_reviewer(request):
    if request.method == "POST":
        manuscript_id = request.POST.get("manuscriptID")
        reviewer_ids = request.POST.getlist("reviewer_ids")
        
        manuscript = get_object_or_404(Manuscripts, id=manuscript_id)

        for reviewer_id in reviewer_ids:
            try:

                user = User.objects.get(id=reviewer_id)

                reviewer = Reviewer.objects.get(auth_user=user)

                reviewer.manuscript_id = manuscript
                reviewer.save()
            except ObjectDoesNotExist:
                print(f"Reviewer with user id {reviewer_id} does not exist.")
                
    
    messages.success(request, 'Reviewer Assigned successfully!')
    return redirect('adminAppointments')


def get_edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    account = appointment.account_id
    manuscript_id = account.student_id.manuscript_id
    researchers_data = Student.objects.filter(manuscript_id=manuscript_id)

    researchers = [
        {
            'id': student.id,
            'name': student.auth_user.get_full_name(),
            'receipt_no': student.receipt_no
        }
        for student in researchers_data
    ]
    college_data = account.college_id

    # Transaction Code Algorithm
    collegeInitials = college_data.college_initials
    preTemplate = "SMCREC"
    yearTemplate = "24"
    latest_transaction = Appointments.objects.filter(institution=collegeInitials).aggregate(
        Max('transaction_id')
    )['transaction_id__max']

    if latest_transaction:
        latest_num = int(latest_transaction.split('-')[-1])
        numTemplate = latest_num + 1
    else:
        numTemplate = 1  

    numTemplate_str = str(numTemplate).zfill(4)
    transaction_code = f"{preTemplate}{yearTemplate}-{collegeInitials}-{numTemplate_str}"

    data = {
        'appointment_id': appointment.id,
        'researchers': researchers,
        'college': college_data.college_initials,
        'transaction_id': transaction_code,
        'email': account.student_id.auth_user.email,
    }

    return JsonResponse(data)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def save_claimStabs(request):
    appID = request.POST.get('appID')
    appointment = get_object_or_404(Appointments, id=appID)
    appointment_instance = Appointments.objects.get(id=appID)
    account = appointment.account_id

    typeOfReview = "Ethics Review"
    status = "Waiting"
    release_date = request.POST.get('release_date')
    received_by = request.POST.get('received_by')
    transactionCode = request.POST.get('transactionCode')

    claimStabs = ClaimStabs.objects.create(
       appointment_id = appointment_instance,
       typeOfReview = typeOfReview, 
       releaseDate = release_date,
       received_by = received_by,
    )

    claimStabs.save()

    appointment.transaction_id = transactionCode
    appointment.status = status
    appointment.save()

    messages.success(request, 'Claim Stabs added successfully!')
    return redirect('adminAppointments')

def get_reviewers_by_college(request, college_id):
    if request.method == "GET":
        try:
            if not College.objects.filter(id=college_id).exists():
                return JsonResponse({"success": False, "message": "College not found"}, status=404)


            reviewers = User.objects.filter(
                id__in=Reviewer.objects.filter(
                    id__in=Accounts.objects.filter(college_id=college_id).values_list('reviewer_id', flat=True)
                ).values_list('auth_user_id', flat=True)
            ).distinct()

            reviewers_data = []
            for reviewer in reviewers:

                reviewer_accounts = Accounts.objects.filter(reviewer_id__auth_user=reviewer)
                if not reviewer_accounts.exists():
                    continue


                schedule_queryset = Schedule.objects.filter(
                    account_id__in=reviewer_accounts
                ).order_by('schedule_date', 'schedule_start_time')


                schedules = [
                    {
                        "date": schedule.schedule_date.strftime('%Y-%m-%d'),
                        "start_time": schedule.schedule_start_time.strftime('%H:%M'),
                        "end_time": schedule.schedule_end_time.strftime('%H:%M'),
                        "type": schedule.schedule_type,
                    }
                    for schedule in schedule_queryset
                ]

                reviewers_data.append({
                    "id": reviewer.id,
                    "first_name": reviewer.first_name,
                    "last_name": reviewer.last_name,
                    "schedules": schedules,
                })

            return JsonResponse({"success": True, "reviewers": reviewers_data}, status=200)

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=400)
def get_view_appointment(request, appointment_id):
    # Fetch the appointment object
    appointment = get_object_or_404(Appointments, id=appointment_id)
    account = appointment.account_id
    manuscript_id = account.student_id.manuscript_id

    # Handle null values for college and email
    college_initials = account.college_id.college_initials if account.college_id else 'N/A'
    email = account.student_id.auth_user.email if account.student_id else 'N/A'

    # Handle null values for basic and supplementary requirements
    basic_requirements = appointment.basicRequirements_id.basicRequirements if appointment.basicRequirements_id else 'N/A'
    supplementary_requirements = appointment.supplementaryRequirements_id.supplementaryRequirements if appointment.supplementaryRequirements_id else 'N/A'

    # Prepare researchers data
    researchers_data = Student.objects.filter(manuscript_id=manuscript_id)
    researchers = [
        {
            'id': student.id,
            'name': student.auth_user.get_full_name(),
            'receipt_no': student.receipt_no
        }
        for student in researchers_data
    ]

    # Fetch ethical risk answers related to the appointment
    ethical_answers_data = EthicalRiskAnswers.objects.filter(appointment_id=appointment)
    ethical_answers = [
        {
            'ethical_question': answer.ethicalQuestions.ethicalQuestions if answer.ethicalQuestions else 'N/A',
            'ethical_answer': answer.ethicalAnswers if answer.ethicalAnswers else 'N/A',
        }
        for answer in ethical_answers_data
    ]

    # Prepare response data
    data = {
        'appointment_id': appointment.id,
        'college': college_initials,
        'transaction_id': appointment.transaction_id,
        'email': email,
        'researchers': researchers,
        'manuscript_id': manuscript_id.id,
        'thesis_title': manuscript_id.thesis_title,
        'thesis_description': manuscript_id.thesis_description,
        'category_name': manuscript_id.category_name.category_name if manuscript_id.category_name else 'N/A',
        'type_of_study': manuscript_id.type_of_study.type_of_study if manuscript_id.type_of_study else 'N/A',
        'study_site': manuscript_id.study_site,
        'basic_requirements': basic_requirements,
        'supplementary_requirements': supplementary_requirements,
        'institution': appointment.institution if appointment.institution else 'N/A',
        'address_of_institution': appointment.address_of_institution if appointment.address_of_institution else 'N/A',
        'status': appointment.status if appointment.status else 'N/A',
        'ethical_answers': ethical_answers,
    }

    return JsonResponse(data)

def adminManuscripts(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    categories = Category.objects.all()
    category_data = []

    studtypes = TypeOfStudy.objects.all()
    studtype_data = []

    basicreqs = BasicRequirements.objects.all()
    basicreq_data = []

    suppreqs = SupplementaryRequirements.objects.all()
    suppreq_data = []


    for category in categories:
        category_data.append({
            'id': category.id,  
            'category_name': category.category_name,
        })

    for studtype in studtypes:
        studtype_data.append({
            'type_of_study': studtype.type_of_study,
        })

    for basicreq in basicreqs:
        basicreq_data.append({
            'basicRequirements': basicreq.basicRequirements,
        })

    for suppreq in suppreqs:
        suppreq_data.append({
            'supplementaryRequirements': suppreq.supplementaryRequirements,
        })


    context = {
        'categories': category_data, 
        'studtype': studtype_data,
        'basicreqs': basicreq_data,
        'suppreqs': suppreq_data,
        'profile_picture': profile_picture,
        'account_type': account_type,
    }

    return render(request, 'admin/adminManuscripts.html', context)


def adminSchedule(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    return render(request, 'admin/adminSchedule.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })

def adminSettings(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    return render(request, 'admin/adminSettings.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })

def adminHelpSupport(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    return render(request, 'admin/adminHelp&Support.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })

def adminColleges(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    colleges = College.objects.all()
    college_data = []

    for college in colleges:
        college_data.append({
            'college_initials': college.college_initials,
            'college_name': college.college_name,
        })

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'colleges': college_data,
    }

    return render(request, 'admin/adminColleges.html', context)



def adminEthicalRiskQuestions(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    
    ethicalRiskQuestions_data = [
        {
            'id': question.id, 
            'ethicalQuestions': question.ethicalQuestions,
        }
        for question in EthicalRiskQuestions.objects.all()
    ]

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'ethicalRiskQuestions': ethicalRiskQuestions_data,
    }

    return render(request, 'admin/adminEthicalQuestions.html', context)

@csrf_exempt
def adminDeleteEthicalRiskQuestions(request, question_id):
    ethical_question = get_object_or_404(EthicalRiskQuestions, id=question_id)
    ethical_question.delete()
    messages.success(request, "Ethical Question deleted successfully!")
    return redirect('adminEthicalRiskQuestions')

@csrf_exempt
def adminEditEthicalRiskQuestions(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        ethical_question_text = request.POST.get('ethical-questions')

        ethical_question = get_object_or_404(EthicalRiskQuestions, id=question_id)
        ethical_question.ethicalQuestions = ethical_question_text
        ethical_question.save()

        messages.success(request, "Ethical Question updated successfully!")
        return redirect('adminEthicalRiskQuestions')




