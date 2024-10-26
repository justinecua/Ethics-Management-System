from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Accounts 
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Schedule, Accounts, Student, Apointments
from django.views.decorators.http import require_POST
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

def studentdashboard(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    username = request.session.get('username', None)
    is_new_user = check_user(request)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'username': username,
        'is_new_user': is_new_user,
    }
    return render (request, 'students/studentdashboard.html', context)

def studentAppointment(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
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
        'account_type': account_type,
    }
    return render(request, 'students/studentSettings.html', context)

def check_user(request):
    if request.user.is_authenticated:
        user_exists = User.objects.filter(id=request.user.id).exists()
        account_exists = Accounts.objects.filter(student_id=request.user.id).exists()
        is_new_user = not (user_exists and account_exists)

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

    Apointments.objects.create(
        appointment_date=appointment_date,
        appointment_name=appointment_name,
        status="Scheduled",
        transaction_id=str(account.student_id)
    )
    messages.success(request, "Appointment scheduled successfully.")
    return redirect('student_appointment')

@login_required
def student_appointment(request):
    # Retrieve the Student instance associated with the logged-in user
    student = get_object_or_404(Student, auth_user=request.user)
    
    # Retrieve the Account linked to this Student
    account = get_object_or_404(Accounts, student_id=student)
    
    # Get all appointments and schedules for this account
    appointments = Apointments.objects.filter(transaction_id=account.student_id)
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


@login_required
def get_appointments(request):
    student = get_object_or_404(Student, auth_user=request.user)
    account = get_object_or_404(Accounts, student_id=student)
    
    # Appointments for this student
    appointments = Apointments.objects.filter(transaction_id=account.student_id)
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
