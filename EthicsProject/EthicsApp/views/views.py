from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from ..models import Event
from ..forms import EventForm

def index(request):
  template = loader.get_template('LandingPage.html')
  return HttpResponse(template.render())

def index1(request):
  template = loader.get_template('ReviewerLogin.html')
  return HttpResponse(template.render())

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'calendar_app/add_event.html', {'form': form})

def calendar_view(request):
    events = Event.objects.all()
    return render(request, 'calendar_app/calendar.html', {'events': events})