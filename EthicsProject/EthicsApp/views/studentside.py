from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Accounts 
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Schedule, Accounts, Student, Appointments, Manuscripts
from django.views.decorators.http import require_POST
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.db.models import Q


def check_thesis_empty(request):
    user_id = request.session.get('id', None)
    thesis_empty = Student.objects.filter(Q(manuscript_id__isnull=True) & Q(auth_user=user_id))

    return thesis_empty

def check_completeProfile(request):
    if request.user.is_authenticated:
        try:
            # Retrieve the authenticated student's record
            studID = Student.objects.get(auth_user=request.user)
            
            # Check if the User model fields (first_name, last_name) are incomplete
            first_name_last_name_incomplete = User.objects.filter(
                Q(id=request.user.id) & (Q(first_name__isnull=True) | Q(first_name="")) & 
                (Q(last_name__isnull=True) | Q(last_name=""))
            ).exists()

            # Check if the Student model fields are incomplete
            other_info_incomplete = Student.objects.filter(
                Q(auth_user=request.user) & 
                (Q(smc_student_no__isnull=True) | Q(mobile_number__isnull=True) | Q(receipt_no__isnull=True))
            ).exists()

            # Combine both checks
            completeProfile_empty = first_name_last_name_incomplete or other_info_incomplete

        except Student.DoesNotExist:
            # Handle case where Student record does not exist
            completeProfile_empty = True

    else:
        completeProfile_empty = False

    return completeProfile_empty


def check_thesis_members(request):
    if not request.user.is_authenticated:
        return False  # Return early if the user is not authenticated

    try:
        # Retrieve the current student object
        student = Student.objects.get(auth_user=request.user)

        # Check if there are other students with the same manuscript_id
        manuscript = student.manuscript_id
        if manuscript:
            other_students = Student.objects.filter(manuscript_id=manuscript).exclude(auth_user=request.user)
            return not other_students.exists()
        return True  # No manuscript linked, so assume no members
    except Student.DoesNotExist:
        return True  # Treat as no members if Student does not exist



@login_required
def studentdashboard(request):
    if request.user.is_authenticated:
        profile_picture = request.session.get('profile_picture', None)
        account_type = request.session.get('account_type', None)
        username = request.session.get('username', None)
        is_new_user = check_user(request)
        thesis_empty_value = check_thesis_empty(request)  
        completeProfile = check_completeProfile(request)
        thesis_no_members = check_thesis_members(request)

        try:
            student = Student.objects.get(auth_user=request.user)
            manuscript = student.manuscript_id if student.manuscript_id else None
            thesis_id = manuscript.id if manuscript else None
        except Student.DoesNotExist:
            student = None
            manuscript = None

        thesis_title = manuscript.thesis_title if manuscript else None

        context = {
            'profile_picture': profile_picture,
            'account_type': account_type,
            'username': username,
            'is_new_user': is_new_user,
            'thesis_empty': thesis_empty_value,
            'thesis_title': thesis_title,
            'thesis_id': thesis_id,
            'completeProfile_empty': completeProfile,
            'thesis_no_members': thesis_no_members,
        }

    return render(request, 'students/studentdashboard.html', context)

def update_thesis_info(request):
    if request.user.is_authenticated:
        try:
            studID = Student.objects.get(auth_user=request.user)
            thesis_title = request.POST.get('thesisTitle')
            thesis_description = request.POST.get('thesisDescription')

            manuscriptCreate = Manuscripts.objects.create(
                thesis_title=thesis_title,
                thesis_description=thesis_description
            )

            studentCreate = Student.objects.get(id=studID.id)
            studentCreate.manuscript_id = manuscriptCreate
            studentCreate.save()

            messages.success(request, "Thesis information has been successfully updated.")
        except Exception as e:
            messages.error(request, f"An error occurred while updating thesis information: {str(e)}")
    
    return redirect('studentdashboard')


def completeProfile(request):
    if request.user.is_authenticated:
        try:
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            smc_student_no = request.POST.get('SMCStudentNo')
            mobile_number = request.POST.get('MobileNumber')
            receipt_no = request.POST.get('ReceiptNo')

            userUpdate = User.objects.get(id=request.user.id)
            userUpdate.first_name = firstname
            userUpdate.last_name = lastname
            userUpdate.save()

            studentUpdate = Student.objects.get(auth_user=request.user)
            studentUpdate.smc_student_no = smc_student_no
            studentUpdate.mobile_number = mobile_number
            studentUpdate.receipt_no = receipt_no
            studentUpdate.save()

            messages.success(request, "Profile information has been successfully updated.")
        except Exception as e:
            messages.error(request, f"An error occurred while updating your profile: {str(e)}")
    
    return redirect('studentdashboard')
 

def studentAppointment(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
   
    is_new_user = check_user(request)
    thesis_empty_value = check_thesis_empty(request)  
    completeProfile = check_completeProfile(request)
    thesis_no_members = check_thesis_members(request)
    
    getting_started_conditions = (
        is_new_user and 
        thesis_empty_value and 
        completeProfile and 
        thesis_no_members
    )

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'getting_started_conditions': getting_started_conditions,
    }
    return render(request, 'students/studentappointment.html', context)


def studentManuscript(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'students/studentmanuscript.html', context)

def studentSettings(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
    }
        
def check_user(request):
    if request.user.is_authenticated:
        session_id = request.session.get('id', None)
        studentId = Student.objects.get(auth_user=session_id)
        is_new_user = Accounts.objects.filter(Q(student_id=studentId) & Q(invite_status="Not Complete"))

        return is_new_user
    else:
        return False


def schedule_list(request):
    schedules = Schedule.objects.all()
    schedule_events = []

    for schedule in schedules:
        schedule_events.append({
            'id': schedule.id,
            'title': schedule.schedule_type,
            'start': f"{schedule.schedule_date}T{schedule.schedule_start_time}",
            'end': f"{schedule.schedule_date}T{schedule.schedule_end_time}",
            'extendedProps': {
                'schedule_id': schedule.id,
                'schedule_type': schedule.schedule_type,
                'schedule_date': schedule.schedule_date,
            }
        })

    return JsonResponse(schedule_events, safe=False)


@require_POST
def save_schedule(request):
    appointment_name = request.POST.get('schedule-type')
    appointment_date = request.POST.get('schedule-date')
    start_time = request.POST.get('schedule-start-time')
    end_time = request.POST.get('schedule-end-time')
    
    # Convert to datetime objects for saving
    appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()

    student = get_object_or_404(Student, auth_user=request.user)
    account = get_object_or_404(Accounts, student_id=student)

    Appointments.objects.create(
        appointment_date=appointment_date,
        appointment_name=appointment_name,
        status="Scheduled",
        transaction_id=str(account.student_id)
    )
    messages.success(request, "Appointment scheduled successfully.")
    return redirect('students_appointments')

@login_required
def student_appointment(request):
    # Retrieve the Student instance associated with the logged-in user
    student = get_object_or_404(Student, auth_user=request.user)
    
    # Retrieve the Account linked to this Student
    account = get_object_or_404(Accounts, student_id=student)
    
    # Get all appointments and schedules for this account
    appointments = Appointments.objects.filter(transaction_id=account.student_id)
    schedules = Schedule.objects.filter(account_id=account)

    # Format the events data to work with FullCalendar
    events = [
        {
            'title': appointment.appointment_name,
            'start': appointment.appointment_date.isoformat(),
            'color': 'yellow' if appointment.status == "Scheduled" else 'gray',
        }
        for appointment in appointments
    ] + [
        {
            'title': schedule.schedule_type,
            'start': f"{schedule.schedule_date}T{schedule.schedule_start_time}",
            'end': f"{schedule.schedule_date}T{schedule.schedule_end_time}",
            'color': 'blue',
        }
        for schedule in schedules
    ]

    # Pass events_json to the context
    context = {
        'events_json': json.dumps(events),
    }
    return render(request, 'students/studentAppointment.html', context)

'''
@login_required
def get_appointments(request):
    student = get_object_or_404(Student, auth_user=request.user)
    account = get_object_or_404(Accounts, student_id=student)
    
    # Appointments for this student
    appointments = Appointments.objects.filter(transaction_id=account.student_id)
    schedules = Schedule.objects.filter(account_id=account)
    
    events = [
        {
            "title": appointment.appointment_name,
            "start": appointment.appointment_date.isoformat(),
            "color": "yellow" if appointment.status == "Scheduled" else "gray",
        }
        for appointment in appointments
    ] + [
        {
            "title": schedule.schedule_type,
            "start": f"{schedule.schedule_date}T{schedule.schedule_start_time}",
            "end": f"{schedule.schedule_date}T{schedule.schedule_end_time}",
            "color": "blue",
        }
        for schedule in schedules
    ]
    
    return JsonResponse(events, safe=False)

'''

def addMemberStudent(request):
    if request.method == 'POST':
        manuscript_id = request.POST.get('manuscriptID')
        manuscript = Manuscripts.objects.get(id=manuscript_id)

        firstnames = request.POST.getlist('firstnames')
        lastnames = request.POST.getlist('lastnames')
        receipt_nos = request.POST.getlist('receipt_nos')
        emails = request.POST.getlist('emails')

        for firstname, lastname, receipt_no, email in zip(firstnames, lastnames, receipt_nos, emails):
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create(
                    username=firstname,
                    email=email,
                    first_name=firstname,
                    last_name=lastname
                )
                user.save()

            student = Student.objects.create(
                auth_user=user,
                smc_student_no=receipt_no,
                receipt_no=receipt_no,
                manuscript_id=manuscript
            )
            student.save()

        messages.success(request, "Members added successfully.")
        return redirect('studentdashboard')

    return redirect('studentdashboard')
