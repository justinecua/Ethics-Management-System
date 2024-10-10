from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.views import View
from .models import Schedule
from datetime import datetime

def edit_schedule(request, scheduleId):
    schedule = get_object_or_404(Schedule, id=scheduleId)
    schedule_type = request.POST.get('schedule-type')
    schedule_date = request.POST.get('schedule-date')
    schedule_start_time = request.POST.get('schedule-start-time')
    schedule_end_time = request.POST.get('schedule-end-time')

    # Validate
    if not all([schedule_type, schedule_date, schedule_start_time, schedule_end_time]):
        messages.error(request, 'All fields are required.')
        return redirect(reverse('adminSchedule', args=[schedule_id]))

    # Convert
    try:
        start_time = datetime.strptime(f"{schedule_date} {schedule_start_time}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{schedule_date} {schedule_end_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        messages.error(request, 'Invalid date or time format.')
        return redirect(reverse('adminSchedule', args=[schedule_id]))

    # Compare
    if start_time >= end_time:
        messages.error(request, 'End time must be after start time.')
        return redirect(reverse('adminSchedule', args=[schedule_id]))

    # Future
    if start_time.date() < datetime.now().date():
        messages.error(request, 'The scheduled date cannot be in the past.')
        return redirect(reverse('adminSchedule', args=[schedule_id]))

    # Overlap
    overlapping_schedules = Schedule.objects.filter(
        schedule_date=schedule_date,
        schedule_start_time__lt=schedule_end_time,
        schedule_end_time__gt=start_time
    ).exclude(id=schedule.id)  

    if overlapping_schedules.exists():
        messages.error(request, 'This schedule overlaps with an existing schedule.')
        return redirect(reverse('adminSchedule', args=[schedule_id]))

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




