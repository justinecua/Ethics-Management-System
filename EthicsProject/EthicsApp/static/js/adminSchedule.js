
let ModalScheduleOverlay = document.getElementById('Modal-Schedule-Overlay');
let EModalScheduleOverlay = document.getElementById('EModal-Schedule-Overlay');
let scheduledate = document.getElementById('schedule-date');
let cancelsched = document.getElementById('cancel-sched');
let ecancelsched = document.getElementById('ecancel-sched');

var calendarEl = document.getElementById('calendar');
var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    height: 'auto',
    events: '/api/schedules/',
    initialDate: new Date(),
    hiddenDays: [0],
    eventClick: function(info) {
        var event = info.event;
        var scheduleId = event.extendedProps.schedule_id;

        EModalScheduleOverlay.style.display = "flex";
        document.getElementById('eschedule-type').value = event.extendedProps.schedule_type || "Available";
        document.getElementById('eschedule-date').value = event.extendedProps.schedule_date;

        document.getElementById('eschedule-start-time').value = 
            event.start ? event.start.getHours().toString().padStart(2, '0') + ':' + event.start.getMinutes().toString().padStart(2, '0') : '';
        
        document.getElementById('eschedule-end-time').value = 
            event.end ? event.end.getHours().toString().padStart(2, '0') + ':' + event.end.getMinutes().toString().padStart(2, '0') : '';

        document.getElementById('edit-schedule-form').action = `/schedules/edit/${scheduleId}/`;
    },
    dateClick: function(info) {
        ModalScheduleOverlay.style.display = "flex";
        scheduledate.value = info.dateStr;
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

ecancelsched.addEventListener('click', function(event){
  event.stopPropagation();
  EModalScheduleOverlay.style.display = "none";
})

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

/*-----------------------Reviewer--------------------*/


var MyScheduleBtn = document.getElementById('MySchedule-btn');
var Reviewerbtn = document.getElementById('Reviewer-btn');
MyScheduleBtn.classList.add('active-btn2');
MyScheduleBtn.style.backgroundColor = "#ffffff";
var ReviewerSchedule = document.getElementById('Reviewer-Schedule');
var ScheduleContent = document.getElementById('Schedule-Content');

function refreshCalendar(calendarInstance) {
    calendarInstance.render();
}

MyScheduleBtn.addEventListener('click', function(){
    ScheduleContent.style.display = "flex";
    ReviewerSchedule.style.display = "none";
    refreshCalendar(calendar);
    MyScheduleBtn.classList.add('active-btn2');
    MyScheduleBtn.style.backgroundColor = "#ffffff";
    Reviewerbtn.classList.remove('active-btn2');
    Reviewerbtn.style.backgroundColor = "";
});

Reviewerbtn.addEventListener('click', function(){
    ScheduleContent.style.display = "none";
    ReviewerSchedule.style.display = "flex";
    refreshCalendar(calendar2);
    MyScheduleBtn.classList.remove('active-btn2');
    MyScheduleBtn.style.backgroundColor = "";
    Reviewerbtn.classList.add('active-btn2');
    Reviewerbtn.style.backgroundColor = "#ffffff";

});

Reviewerbtn.addEventListener('click', function(){
    ScheduleContent.style.display = "none";
    ReviewerSchedule.style.display = "flex";
    refreshCalendar(calendar2);
    MyScheduleBtn.classList.remove('active-btn2');
    MyScheduleBtn.style.backgroundColor = "";
    Reviewerbtn.classList.add('active-btn2');
    Reviewerbtn.style.backgroundColor = "#ffffff";

});

var calendarEl2 = document.getElementById('calendar2');
var calendar2 = new FullCalendar.Calendar(calendarEl2, {
    initialView: 'dayGridMonth',
    height: 'auto',
    hiddenDays: [0],
    initialDate: new Date()
});
calendar2.render();

var monthSelect2 = document.getElementById('monthSelect2');
var yearSelect2 = document.getElementById('yearSelect2');
var currentYear2 = new Date().getFullYear();
var currentMonth2 = new Date().getMonth();
var currentDate2 = new Date().getDate();

for (var year = currentYear - 5; year <= currentYear2 + 5; year++) {
    var option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect2.appendChild(option);
}

monthSelect2.value = currentMonth2;
yearSelect2.value = currentYear2;

function updateMonthYearSelect2() {
    var currentCalendarDate2 = calendar2.getDate();
    monthSelect2.value = currentCalendarDate2.getMonth();
    yearSelect2.value = currentCalendarDate2.getFullYear();
}

monthSelect2.addEventListener('change', function () {
    var selectedMonth2 = parseInt(this.value);
    var selectedYear2 = parseInt(yearSelect2.value);
    calendar2.gotoDate(new Date(selectedYear2, selectedMonth2, currentDate2));
});

yearSelect2.addEventListener('change', function () {
    var selectedMonth2 = parseInt(monthSelect2.value);
    var selectedYear2 = parseInt(this.value);
    calendar2.gotoDate(new Date(selectedYear2, selectedMonth2, currentDate2));
});


var monthViewButton2 = document.getElementById('monthView2');
monthViewButton2.classList.add('active-btn2');
monthViewButton2.style.backgroundColor = "#ffffff";

var buttons2 = document.querySelectorAll('.RSC-CalendarView button');
buttons2.forEach(function(button2) {
    button2.addEventListener('click', function() {
        buttons2.forEach(function(btn2) {
            btn2.classList.remove('active-btn2');
            btn2.style.backgroundColor = "";
        });

        this.classList.add('active-btn2');
        this.style.backgroundColor = '#ffffff';

          if (this.id === 'dayView2') {
            calendar2.changeView('timeGridDay');
        } else if (this.id === 'weekView2') {
            calendar2.changeView('timeGridWeek');
        } else if (this.id === 'monthView2') {
            calendar2.changeView('dayGridMonth');
        }
    });
});

document.getElementById('prevSchedule2').addEventListener('click', function() {
    calendar2.prev();
    updateMonthYearSelect2();
});

document.getElementById('nextSchedule2').addEventListener('click', function() {
    calendar2.next();
    updateMonthYearSelect2();
});

/*-------------------------------------------------------------------*/
let MSContainer = document.getElementById('MS-Container');
let EMSContainer = document.getElementById('EMS-Container');


document.addEventListener('click', function(event) {
    if (event.target === ModalScheduleOverlay) {
        ModalScheduleOverlay.style.display = "none";
    }
    if (event.target === EModalScheduleOverlay) {
        EModalScheduleOverlay.style.display = "none";
    }
});
