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

from django.shortcuts import render
from .models import Appointments, Accounts, Student, Manuscripts
import os

def reviewerManuscript(request):
    profile_picture = request.session.get('profile_picture', None)
    account_type = request.session.get('account_type', None)
    user_id = request.session.get('id', None)

    manuscript = None
    appointments = []
    if user_id:
        try:
            # Fetch Reviewer and associated manuscript
            reviewer = Reviewer.objects.get(auth_user__id=user_id)
            manuscript = reviewer.manuscript_id

            # Fetch appointments for the reviewer
            account = Accounts.objects.get(reviewer_id=reviewer)
            appointments = Appointments.objects.filter(account_id=account)
        except Reviewer.DoesNotExist:
            print("Reviewer not found.")
        except Accounts.DoesNotExist:
            print("Account not found for the reviewer.")
        except Appointments.DoesNotExist:
            print("No appointments found.")
        except Manuscripts.DoesNotExist:
            print("No manuscript found.")

    context = {
        'profile_picture': profile_picture,
        'account_type': account_type,
        'appointments': appointments,
        'manuscript': manuscript,
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
from .models import Schedule, Account_Type, Reviewer
from django.http import JsonResponse

class ReviewerScheduleView(View): 
    def post(self, request):
        userId = request.session.get('id', None)
        reviewer_id = Reviewer.objects.get(auth_user_id=userId)
        accId = Accounts.objects.get(reviewer_id=reviewer_id)

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


        try:
            schedule = Schedule(
                account_id=accId,
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
        reviewer_id = Reviewer.objects.get(auth_user_id=userId)
        accId = Accounts.objects.get(reviewer_id=reviewer_id)
        schedules = Schedule.objects.filter(schedule_date__gte=today, account_id=accId)

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

