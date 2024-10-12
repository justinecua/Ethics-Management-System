from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Schedule, Account_Type, Accounts, Reviewer, Student
from datetime import datetime
from django.contrib import messages 
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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

def edit_schedule(request, scheduleId):
    schedule = get_object_or_404(Schedule, id=scheduleId)
    schedule_type = request.POST.get('eschedule-type')
    schedule_date = request.POST.get('eschedule-date')
    schedule_start_time = request.POST.get('eschedule-start-time')
    schedule_end_time = request.POST.get('eschedule-end-time')

    if not all([schedule_type, schedule_date, schedule_start_time, schedule_end_time]):
        messages.error(request, 'All fields are required.')
        return redirect(reverse('adminSchedule'))

    try:
        start_time = datetime.strptime(f"{schedule_date} {schedule_start_time}", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(f"{schedule_date} {schedule_end_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        messages.error(request, 'Invalid date or time format.')
        return redirect(reverse('adminSchedule'))

    if start_time >= end_time:
        messages.error(request, 'End time must be after start time.')
        return redirect(reverse('adminSchedule'))

    if start_time.date() < datetime.now().date():
        messages.error(request, 'The scheduled date cannot be in the past.')
        return redirect(reverse('adminSchedule'))

    overlapping_schedules = Schedule.objects.filter(
        schedule_date=schedule_date,
        schedule_start_time__lt=schedule_end_time,
        schedule_end_time__gt=start_time
    ).exclude(id=schedule.id)  

    if overlapping_schedules.exists():
        messages.error(request, 'This schedule overlaps with an existing schedule.')
        return redirect(reverse('adminSchedule'))

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








































































































#---------------------------------Justine---------------------------------
def send_invitation_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        role = request.POST.get('role')

        if not email or not role:
            messages.error(request, "Email and role must be provided.")
            return redirect('adminAccounts')

        invite_status = "Pending"
        user, created = User.objects.get_or_create(email=email, username=email)

        if role == 'Admin' and not user.is_superuser:
            user.is_superuser = True
            user.is_staff = True
            user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(str(user.pk).encode())
        invite_link = request.build_absolute_uri(reverse('set_password', kwargs={'uidb64': uid, 'token': token}))

        context = {
            'user': user,
            'invite_link': invite_link,
            'role': role
        }

        html_content = render_to_string('emails/invite_gmailaccounts.html', context)
        plain_message = strip_tags(html_content)

        mail = EmailMultiAlternatives(
            subject="Invitation to join",
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )

        mail.attach_alternative(html_content, "text/html")

        try:
            mail.send(fail_silently=False)
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")
            return redirect('adminAccounts')

        if role == 'Reviewer':
            try:
                reviewer_account_type = Account_Type.objects.get(Account_type='Reviewer')
                reviewer = Reviewer.objects.create(auth_user=user)
                Accounts.objects.create(
                    reviewer_id=reviewer,
                    account_typeid=reviewer_account_type,
                    invite_status=invite_status
                )
            except Account_Type.DoesNotExist:
                messages.error(request, "Reviewer account type does not exist.")
                return redirect('adminAccounts')
            except Exception as e:
                messages.error(request, f"Error creating reviewer account: {str(e)}")
                return redirect('adminAccounts')

        elif role == 'Admin':
            try:
                admin_account_type = Account_Type.objects.get(Account_type='Admin')
                admin = Reviewer.objects.create(auth_user=user)
                Accounts.objects.create(
                    reviewer_id=admin,
                    account_typeid=admin_account_type,
                    invite_status=invite_status
                )
            except Account_Type.DoesNotExist:
                messages.error(request, "Admin account type does not exist.")
                return redirect('adminAccounts')
            except Exception as e:
                messages.error(request, f"Error creating admin account: {str(e)}")
                return redirect('adminAccounts')

        return redirect('adminAccounts')

    messages.error(request, "Invalid request method.")
    return redirect('adminAccounts')

def set_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                login(request, user)
                return redirect('success_url') 
        else:
            form = SetPasswordForm(user)
        return render(request, 'emails/set_password.html', {'form': form})
    else:
        return render(request, 'emails/password_reset_invalid.html')

