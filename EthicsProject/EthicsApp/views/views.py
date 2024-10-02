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