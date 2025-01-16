from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.contrib import messages
from .models import Student, Accounts, Reviewer, Account_Type, College, Category, TypeOfStudy, BasicRequirements, SupplementaryRequirements, EthicalRiskQuestions, Appointments, Schedule, ClaimStabs
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Count, F
import json
from .models import *from .models import *
from django.views import View
from datetime import datetime


def get_google_profile_picture(user):
    social_account = user.socialaccount_set.filter(provider='google').first()
    if social_account:
        return social_account.extra_data.get('picture')
    return None


def adminDashboard(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    # Data aggregation
    manuscript_count = Manuscripts.objects.count()
    student_count = Student.objects.count()
    reviewer_count = Reviewer.objects.count()
    college_count = College.objects.count()
    schedule_count = Schedule.objects.count()
    appointment_count = Appointments.objects.count()

    # Manuscripts by category and type of study
    manuscripts_by_category = Manuscripts.objects.values('category_name_id__category_name').annotate(total=Count('id'))
    manuscripts_by_study_type = Manuscripts.objects.values('type_of_study_id__type_of_study').annotate(total=Count('id'))

    # Accounts by college
    accounts_by_college = Accounts.objects.values('college_id__college_initials').annotate(total=Count('id'))

    # Notifications and comments counts
    notification_count = Notification.objects.count()
    comment_count = Comments.objects.count()

    # Prepare counts dictionary
    counts = {
        "Manuscripts": manuscript_count,
        "Students": student_count,
        "Reviewers": reviewer_count,
        "Colleges": college_count,
        "Schedules": schedule_count,
        "Appointments": appointment_count,
    }

    # Prepare data for JSON-safe rendering
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'counts': counts,
        'manuscripts_by_category': json.dumps(list(manuscripts_by_category)),
        'manuscripts_by_study_type': json.dumps(list(manuscripts_by_study_type)),
        'accounts_by_college': json.dumps(list(accounts_by_college)),
        'notification_count': notification_count,
        'comment_count': comment_count,
    }
    return render(request, 'admin/adminDashboard.html', context)


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Reviewer, Accounts, Account_Type
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch, Q




def adminAccounts(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    # Get the search query from the request
    search_query = request.GET.get('search', '').strip()

    # Querysets for Students, Reviewers, and Admins
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

    # Apply search filters
    if search_query:
        students = students.filter(
            Q(auth_user__username__icontains=search_query) |
            Q(auth_user__first_name__icontains=search_query) |
            Q(auth_user__last_name__icontains=search_query) |
            Q(auth_user__email__icontains=search_query)
        )
        reviewers = reviewers.filter(
            Q(auth_user__username__icontains=search_query) |
            Q(auth_user__first_name__icontains=search_query) |
            Q(auth_user__last_name__icontains=search_query) |
            Q(auth_user__email__icontains=search_query)
        )
        admins = admins.filter(
            Q(auth_user__username__icontains=search_query) |
            Q(auth_user__first_name__icontains=search_query) |
            Q(auth_user__last_name__icontains=search_query) |
            Q(auth_user__email__icontains=search_query)
        )

    # Add profile pictures
    for student in students:
        student.google_picture = get_google_profile_picture(student.auth_user)
    for reviewer in reviewers:
        reviewer.google_picture = get_google_profile_picture(reviewer.auth_user)
    for admin in admins:
        admin.google_picture = get_google_profile_picture(admin.auth_user)

    # Handle invitation
    if request.method == 'POST' and 'invite' in request.POST:
        email = request.POST.get('email', '').strip()
        account_type = request.POST.get('account_type', '').strip()

        if email and account_type:
            # Create a new user invitation logic
            try:
                # Check if email already exists
                if Accounts.objects.filter(auth_user__email=email).exists():
                    return HttpResponse("This email is already registered.")
                
                # Generate invitation logic (e.g., sending an email)
                subject = f"Invitation to Join as {account_type}"
                message = f"Dear User,\n\nYou are invited to join as a {account_type}.\n\nBest Regards!"
                from_email = 'admin@example.com'

                # Send an email invitation
                send_mail(subject, message, from_email, [email])
                
                # Optionally, store some information in the database for the invitation (e.g., a pending user)
                # PendingUser.objects.create(email=email, account_type=account_type)

                return HttpResponse("Invitation sent successfully.")

            except Exception as e:
                return HttpResponse(f"Error sending invitation: {str(e)}")

    # Paginate Students
    student_page_number = request.GET.get('students_page', 1)
    student_paginator = Paginator(students, 10)
    try:
        students_page = student_paginator.page(student_page_number)
    except (EmptyPage, PageNotAnInteger):
        students_page = student_paginator.page(1)

    # Paginate Reviewers
    reviewer_page_number = request.GET.get('reviewers_page', 1)
    reviewer_paginator = Paginator(reviewers, 10)
    try:
        reviewers_page = reviewer_paginator.page(reviewer_page_number)
    except (EmptyPage, PageNotAnInteger):
        reviewers_page = reviewer_paginator.page(1)

    # Paginate Admins
    admin_page_number = request.GET.get('admins_page', 1)
    admin_paginator = Paginator(admins, 10)
    try:
        admins_page = admin_paginator.page(admin_page_number)
    except (EmptyPage, PageNotAnInteger):
        admins_page = admin_paginator.page(1)

    accountType = Account_Type.objects.exclude(Account_type='Student')

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'students_page': students_page,
        'reviewers_page': reviewers_page,
        'admins_page': admins_page,
        'accountTypes': accountType,
        'search_query': search_query,
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


def remove_reviewer(request, reviewer_id):
    # Check if the user is authorized to perform this action
    if request.method == 'POST':
        try:
            reviewer = Reviewer.objects.get(id=reviewer_id)
            reviewer.delete()
            return JsonResponse({'success': True})
        except Reviewer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reviewer not found'})

def resend_invite(request, reviewer_id):
    # Logic to resend the invite (depending on your invite system)
    if request.method == 'POST':
        try:
            reviewer = Reviewer.objects.get(id=reviewer_id)
            # Your logic to resend the invite goes here
            return JsonResponse({'success': True})
        except Reviewer.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reviewer not found'})
        

