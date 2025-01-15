from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .models import Accounts 
from django.contrib.auth.models import User


def reviewerdashboard(request):
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
    return render (request, 'Reviewer/reviewerDashboard.html', context)

def reviewerManuscript(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'Reviewer/reviewerManuscripts.html', context)

def reviewerSettings(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'Reviewer/reviewerSettings.html', context)

def reviewerSchedule(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
        
    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
    }
    return render(request, 'Reviewer/reviewerSchedule.html', context)

def check_user(request):
    if request.user.is_authenticated:
        user_exists = User.objects.filter(id=request.user.id).exists()
        account_exists = Accounts.objects.filter(student_id=request.user.id).exists()
        is_new_user = not (user_exists and account_exists)

        return is_new_user
    else:
        return False


#reviewer schedule
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import Schedule
from django.http import JsonResponse
class ReviewerScheduleView(View): 
    def post(self, request):
        userId = request.session.get('id', None)
        accId = "3" 
        acc_instance = Account_Type.objects.get(id=accId)
        schedule_type = request.POST.get('schedule-type')
        schedule_date = request.POST.get('schedule-date')
        schedule_start_time = request.POST.get('schedule-start-time')
        schedule_end_time = request.POST.get('schedule-end-time')
        slot = request.POST.get('slots')

        print(accId)
        if not schedule_type or not schedule_date or not schedule_start_time or not schedule_end_time:
            messages.error(request, 'All fields are required.')
            return redirect('reviewerSchedule')

        start_time_str = f"{schedule_date} {schedule_start_time}"
        end_time_str = f"{schedule_date} {schedule_end_time}"

        try:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            messages.error(request, 'Invalid date or time format.')
            return redirect('reviewerSchedule')

        if start_time >= end_time:
            messages.error(request, 'End time must be after start time.')
            return redirect('reviewerSchedule')

        if start_time.date() < datetime.now().date():
            messages.error(request, 'The scheduled date cannot be in the past.')
            return redirect('reviewerSchedule')

        overlapping_schedules = Schedule.objects.filter(
            schedule_date=schedule_date,
            schedule_start_time__lt=schedule_end_time,
            schedule_end_time__gt=schedule_start_time
        )

        if overlapping_schedules.exists():
            messages.error(request, 'This schedule overlaps with an existing schedule.')
            return redirect('reviewerSchedule')

        try:
            schedule = Schedule(
                account_id=acc_instance,
                schedule_type=schedule_type,
                schedule_date=schedule_date,
                schedule_start_time=schedule_start_time,
                schedule_end_time=schedule_end_time,
                slot = slot,
            )
            schedule.save()
            messages.success(request, 'Schedule added successfully!')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

        return redirect('reviewerSchedule')

class ReviewerScheduleDataView(View):
    def get(self, request):
        today = datetime.now().date()
        userId = request.session.get('id', None)
        accId = "3" 
        acc_instance = Account_Type.objects.get(id=accId)
        schedules = Schedule.objects.filter(schedule_date__gte=today, account_id=acc_instance)

        events = []

        for schedule in schedules:
            if schedule.schedule_date and schedule.schedule_start_time and schedule.schedule_end_time:
                start = f"{schedule.schedule_date}T{schedule.schedule_start_time}"
                end = f"{schedule.schedule_date}T{schedule.schedule_end_time}"
                
                events.append({
                    'title': schedule.schedule_type,
                    'start': start,
                    'end': end,
                    'slot': schedule.slot,
                    'extendedProps': {
                        'schedule_type': schedule.schedule_type,
                        'schedule_id': schedule.id,
                        'schedule_date': schedule.schedule_date.isoformat(),
                    },
                })
            else:
                events.append({
                    'title': 'Incomplete',
                    'start': None,
                    'end': None,
                    'extendedProps': {
                        'schedule_type': 'Incomplete',
                        'schedule_id': None,
                        'schedule_date': None,
                    },
                })

        return JsonResponse(events, safe=False)



def reviewerSchedule(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)

    return render(request, 'admin/adminSchedule.html', {
        'profile_picture': profile_picture,
        'account_type': account_type
    })
