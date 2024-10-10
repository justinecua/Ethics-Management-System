from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Schedule
from datetime import datetime
from django.contrib import messages 

def index(request):
    return render(request, 'LandingPage.html')

def schedule_view(request):
    schedules = Schedule.objects.all()  
    return render(request, 'Reviewer/CalendarSchedule.html', {'schedules': schedules}) 

def schedule_list(request):
    schedules = Schedule.objects.all()
    return render(request, 'Reviewer/ScheduleList.html', {'schedules': schedules})

def AddSchedule(request):
    if request.method == 'POST':
        schedname = request.POST.get('schedname', "Unnamed Schedule")
        datetime_str = request.POST.get('datetime')
        description = request.POST.get('description', '')

        if datetime_str:
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
            schedule = Schedule(schedname=schedname, datetime=datetime_obj, description=description)
            schedule.save()
            
            return JsonResponse({'success': True}) 
        else:
            return JsonResponse({'success': False, 'error': 'Invalid date/time'}, status=400)

    # Handle GET request if necessary
    return render(request, 'Reviewer/AddSchedule.html')

def AddSchedule2(request):
    if request.method == 'POST':
        schedname = request.POST.get('schedname', "Unnamed Schedule")
        datetime_str = request.POST.get('datetime')
        description = request.POST.get('description', '')

        if datetime_str:
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
            schedule = Schedule(schedname=schedname, datetime=datetime_obj, description=description)
            schedule.save()
            
        messages.success(request, 'Schedule added successfully!')
            
    return render(request, 'Reviewer/AddSchedule.html')


def update_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if request.method == 'POST':
        schedule.schedname = request.POST.get('schedname', "Unnamed Schedule")
        datetime_str = request.POST.get('datetime')
        schedule.description = request.POST.get('description')

        if datetime_str:
            schedule.datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        
        schedule.save()
        return HttpResponseRedirect(reverse('schedule_list'))
    
    return render(request, 'Reviewer/UpdateSchedule.html', {'schedule': schedule})

def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.delete()
    return HttpResponseRedirect(reverse('schedule_list'))

def dashboard (request):
    schedules = Schedule.objects.all()
    return render (request, 'Reviewer/dashboard.html', {'schedules':schedules})

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from .models import Schedule
from datetime import datetime

def edit_schedule(request, scheduleId):
    schedule = get_object_or_404(Schedule, id=scheduleId)
    schedule_type = request.POST.get('eschedule-type')
    schedule_date = request.POST.get('eschedule-date')
    schedule_start_time = request.POST.get('eschedule-start-time')
    schedule_end_time = request.POST.get('eschedule-end-time')

    # Validate
    if not all([schedule_type, schedule_date, schedule_start_time, schedule_end_time]):
        messages.error(request, 'All fields are required.')
        return redirect(reverse('adminSchedule'))

    # Convert
    try:
        start_time = datetime.strptime(f"{schedule_date} {schedule_start_time}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{schedule_date} {schedule_end_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        messages.error(request, 'Invalid date or time format.')
        return redirect(reverse('adminSchedule'))

    # Compare
    if start_time >= end_time:
        messages.error(request, 'End time must be after start time.')
        return redirect(reverse('adminSchedule'))

    # Future
    if start_time.date() < datetime.now().date():
        messages.error(request, 'The scheduled date cannot be in the past.')
        return redirect(reverse('adminSchedule'))

    # Overlap
    overlapping_schedules = Schedule.objects.filter(
        schedule_date=schedule_date,
        schedule_start_time__lt=schedule_end_time,
        schedule_end_time__gt=start_time
    ).exclude(id=schedule.id)  

    if overlapping_schedules.exists():
        messages.error(request, 'This schedule overlaps with an existing schedule.')
        return redirect(reverse('adminSchedule'))

    # Save changes
    try:
        schedule.schedule_type = schedule_type
        schedule.schedule_date = schedule_date
        schedule.schedule_start_time = schedule_start_time
        schedule.schedule_end_time = schedule_end_time
        schedule.save()
        messages.success(request, 'Schedule updated successfully!')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('adminSchedule')

