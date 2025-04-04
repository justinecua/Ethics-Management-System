let ModalScheduleOverlay = document.getElementById('Modal-Schedule-Overlay');
let EModalScheduleOverlay = document.getElementById('EModal-Schedule-Overlay');
let scheduledate = document.getElementById('schedule-date');
let cancelsched = document.getElementById('cancel-sched');
let ecancelsched = document.getElementById('ecancel-sched');

// Reviewer Calendar Initialization
var calendarEl2 = document.getElementById('calendar2');
var calendar2 = new FullCalendar.Calendar(calendarEl2, {
    initialView: 'dayGridMonth',
    height: 'auto',
    events: '/api/schedulesReviewer/',  // This should call the new view that returns reviewer data
    initialDate: new Date(),
    hiddenDays: [0], // Hide Sundays
    eventClick: function(info) {
        var event = info.event;
        var scheduleId = event.extendedProps.schedule_id;

        // Open modal for editing reviewer schedule
        EModalScheduleOverlay.style.display = "flex";
        document.getElementById('eschedule-type').value = event.extendedProps.schedule_type || "Available";
        document.getElementById('eschedule-date').value = event.extendedProps.schedule_date;
        document.getElementById('eslots').value = event.extendedProps.slot;

        document.getElementById('eschedule-start-time').value = 
            event.start ? event.start.toISOString().slice(11, 16) : '';

        document.getElementById('eschedule-end-time').value = 
            event.end ? event.end.toISOString().slice(11, 16) : '';

        document.getElementById('edit-schedule-form').action = `/schedules/edit/${scheduleId}/`;
    },
    eventContent: function(arg) {
        var startTime = arg.event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
        var endTime = arg.event.end ? arg.event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true }) : '';
        var scheduleTypeClass = arg.event.extendedProps.schedule_type === "Available" ? "Available" : "Not-Available";
        var scheduleId = arg.event.extendedProps.schedule_id;
        var profilePicture = arg.event.extendedProps.profile_picture; // Retrieve the profile picture URL
    
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
    
        // Create an element for the profile picture
        if (profilePicture) {
            var profilePicElement = document.createElement('img');
            profilePicElement.src = profilePicture;  // Use the reviewer's profile picture
            profilePicElement.className = 'profile-picture';  // Add a class for styling
            eventContainer.appendChild(profilePicElement);
        }
    
        return { domNodes: [eventContainer] };
    }
});


// Render the calendar
calendar2.render();

// Link dropdown controls to Reviewer Calendar
var monthSelect2 = document.getElementById('monthSelect2');
var yearSelect2 = document.getElementById('yearSelect2');

monthSelect2.value = new Date().getMonth();
yearSelect2.value = new Date().getFullYear();

monthSelect2.addEventListener('change', function () {
    var selectedMonth = parseInt(this.value);
    var selectedYear = parseInt(yearSelect2.value);
    calendar2.gotoDate(new Date(selectedYear, selectedMonth, 1));
    calendar2.refetchEvents(); // Ensure events are refreshed
});

yearSelect2.addEventListener('change', function () {
    var selectedMonth = parseInt(monthSelect2.value);
    var selectedYear = parseInt(this.value);
    calendar2.gotoDate(new Date(selectedYear, selectedMonth, 1));
    calendar2.refetchEvents(); // Ensure events are refreshed
});

// Navigation Buttons for Reviewer Calendar
document.getElementById('prevSchedule2').addEventListener('click', function() {
    calendar2.prev();
    calendar2.refetchEvents(); // Refresh events when navigating
});

document.getElementById('nextSchedule2').addEventListener('click', function() {
    calendar2.next();
    calendar2.refetchEvents(); // Refresh events when navigating
});

// Reviewer Button Click Logic
document.getElementById('Reviewer-btn').addEventListener('click', function () {
    // Show the reviewer schedule section
    document.getElementById('Reviewer-Schedule').style.display = 'block';
    document.getElementById('Schedule-Content').style.display = 'none';
    
    // Refetch the events for the calendar
    calendar2.refetchEvents();
});

// Close modals when clicking outside
document.addEventListener('click', function(event) {
    if (event.target === ModalScheduleOverlay) {
        ModalScheduleOverlay.style.display = "none";
    }
    if (event.target === EModalScheduleOverlay) {
        EModalScheduleOverlay.style.display = "none";
    }
});
