
let ModalScheduleOverlay = document.getElementById('Modal-Schedule-Overlay');
let EModalScheduleOverlay = document.getElementById('EModal-Schedule-Overlay');
let scheduledate = document.getElementById('schedule-date');
let cancelsched = document.getElementById('cancel-sched');
let ecancelsched = document.getElementById('ecancel-sched');

var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    height: 'auto',
    events: '/api/get_appointments/', 
    initialDate: new Date(),
    hiddenDays: [0],
    eventClick: function(info) {
        var event = info.event;
        var scheduleId = event.extendedProps.schedule_id;

    
        EModalScheduleOverlay.style.display = "flex";
        document.getElementById('eschedule-type').value = event.extendedProps.schedule_type || "Available";
        document.getElementById('eschedule-date').value = event.extendedProps.schedule_date;

        document.getElementById('eschedule-start-time').value = 
            event.start ? event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }) : '';
        
        document.getElementById('eschedule-end-time').value = 
            event.end ? event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }) : '';

        document.getElementById('edit-schedule-form').action = `/schedules/edit/${scheduleId}/`;
    },
    dateClick: function(info) {
      if (getting_started_conditions) {
          let gettingStartedConditionErrorOverlay = document.getElementById('gettingStartedConditionError-Overlay');
          gettingStartedConditionErrorOverlay.style.display = "flex";
      } else {
          ModalScheduleOverlay.style.display = "flex";
          scheduledate.value = info.dateStr;
      }
    },

    eventContent: function(arg) {
        var startTime = arg.event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
        var endTime = arg.event.end ? arg.event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }) : '';
        var scheduleTypeClass = arg.event.extendedProps.schedule_type === "Available" ? "Available" : "Not-Available";
        var scheduleId = arg.event.extendedProps.schedule_id;
    
        var deleteButton = document.createElement('img');
        deleteButton.className = 'delete-event';
        deleteButton.src = '../static/images/Delete-2--Streamline-Block---Free.png';
        deleteButton.dataset.scheduleId = scheduleId;
    
        deleteButton.addEventListener('click', function(event) {
            event.stopPropagation();
            deleteEvent(scheduleId);
        });
    
        var eventContainer = document.createElement('div');
        eventContainer.className = `event-container ${scheduleTypeClass}`;
    
        var availabilityIndicator = document.createElement('div');
        availabilityIndicator.className = `availability-indicator ${arg.event.extendedProps.schedule_type === 'Available' ? 'green' : 'red'}`;
    
        var eventTime = document.createElement('div');
        eventTime.className = 'event-time';
        eventTime.innerText = `${startTime} - ${endTime}`;
    
        availabilityIndicator.append(eventTime);
        eventContainer.appendChild(availabilityIndicator);
    
        return { domNodes: [eventContainer] };
    },
    
});

calendar.render();

cancelsched.addEventListener('click', function(event){
  event.stopPropagation();
  ModalScheduleOverlay.style.display = "none";
})

/*
ecancelsched.addEventListener('click', function(event){
  event.stopPropagation();
  EModalScheduleOverlay.style.display = "none";
})

*/
var monthSelect = document.getElementById('monthSelect');
var yearSelect = document.getElementById('yearSelect');
var currentYear = new Date().getFullYear();
var currentMonth = new Date().getMonth();
var currentDate = new Date().getDate();

for (var year = currentYear - 5; year <= currentYear + 5; year++) {
    var option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
}

monthSelect.value = currentMonth;
yearSelect.value = currentYear;

function updateMonthYearSelect() {
    var currentCalendarDate = calendar.getDate();
    monthSelect.value = currentCalendarDate.getMonth();
    yearSelect.value = currentCalendarDate.getFullYear();
}

monthSelect.addEventListener('change', function () {
    var selectedMonth = parseInt(this.value);
    var selectedYear = parseInt(yearSelect.value);
    calendar.gotoDate(new Date(selectedYear, selectedMonth, currentDate));
});

yearSelect.addEventListener('change', function () {
    var selectedMonth = parseInt(monthSelect.value);
    var selectedYear = parseInt(this.value);
    calendar.gotoDate(new Date(selectedYear, selectedMonth, currentDate));
});

var monthViewButton = document.getElementById('monthView');
monthViewButton.classList.add('active-btn');
monthViewButton.style.backgroundColor = "#ffffff";

var buttons = document.querySelectorAll('.SC-CalendarView button');
buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        buttons.forEach(function(btn) {
            btn.classList.remove('active-btn');
            btn.style.backgroundColor = "";
        });

        this.classList.add('active-btn');
        this.style.backgroundColor = '#ffffff';

        if (this.id === 'dayView') {
            calendar.changeView('timeGridDay');
        } else if (this.id === 'weekView') {
            calendar.changeView('timeGridWeek');
        } else if (this.id === 'monthView') {
            calendar.changeView('dayGridMonth');
        }
        updateMonthYearSelect();
    });
});

document.getElementById('prevSchedule').addEventListener('click', function() {
    calendar.prev();
    updateMonthYearSelect();
});

document.getElementById('nextSchedule').addEventListener('click', function() {
    calendar.next();
    updateMonthYearSelect();
});



/*-------------------------------------------------------------------*/
let MSContainer = document.getElementById('MS-Container');
let EMSContainer = document.getElementById('EMS-Container');
let gettingStartedConditionErrorOverlay = document.getElementById('gettingStartedConditionError-Overlay');
let NotCompleteProfilebtn = document.getElementById('NotCompleteProfile-btn');

document.addEventListener('click', function(event) {
    if (event.target === ModalScheduleOverlay) {
        ModalScheduleOverlay.style.display = "none";
    }
    if (event.target === EModalScheduleOverlay) {
        EModalScheduleOverlay.style.display = "none";
    }
    if (event.target === gettingStartedConditionErrorOverlay) {
        gettingStartedConditionErrorOverlay.style.display = "none";
    }
});

NotCompleteProfilebtn.addEventListener('click', function(){
  gettingStartedConditionErrorOverlay.style.display = "none";
})

