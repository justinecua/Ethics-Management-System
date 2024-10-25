from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Accounts 
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Schedule, Accounts, Student
from django.views.decorators.http import require_POST
from datetime import datetime
from django.shortcuts import get_object_or_404

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


def student_appointment(request):
    return render(request, 'students/studentAppointment.html')

@require_POST
def save_schedule(request):
    schedule_type = request.POST.get('schedule-type')
    schedule_date = request.POST.get('schedule-date')
    start_time = request.POST.get('schedule-start-time')
    end_time = request.POST.get('schedule-end-time')
    
    # Convert to datetime objects for saving
    schedule_date = datetime.strptime(schedule_date, '%Y-%m-%d').date()
    start_time = datetime.strptime(start_time, '%H:%M').time()
    end_time = datetime.strptime(end_time, '%H:%M').time()
    
    # First, retrieve the Student instance associated with the logged-in user
    student = get_object_or_404(Student, auth_user=request.user)
    
    # Next, retrieve the Accounts instance linked to this Student
    account = get_object_or_404(Accounts, student_id=student)
    
    # Save the schedule with the user's account information
    Schedule.objects.create(
        account_id=account,
        schedule_type=schedule_type,
        schedule_date=schedule_date,
        schedule_start_time=start_time,
        schedule_end_time=end_time
    )

    return redirect('student_appointment')  # Redirect back to the calendar page
