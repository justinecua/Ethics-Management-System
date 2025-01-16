from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from django.contrib import messages
from .models import Student, Accounts, Reviewer, Account_Type, College, Category, TypeOfStudy, BasicRequirements, SupplementaryRequirements, EthicalRiskQuestions, Appointments
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
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

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
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
    data = {
        'appointment_id': appointment.id,
        'researchers': researchers,
        'college': college_data.college_initials,
        'transaction_id': appointment.transaction_id,
        'email': account.student_id.auth_user.email,
    }

    # Return the data as a JSON response
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

    # Retrieve all ethical risk questions and include the ID and question text in the context
    ethicalRiskQuestions_data = [
        {
            'id': question.id,  # Include the ID here
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
        

