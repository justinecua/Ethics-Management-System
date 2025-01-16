let ModalEditAppointmentOverlay = document.getElementById('Modal-Edit-Appointment-Overlay');
let cancelButton = document.getElementById('cancel-editapp-btn');
let ModalAssignAppOverlay = document.getElementById('Modal-Assign-App-Overlay');
let cancelassignappbtn = document.getElementById('cancel-assign-app-btn');

cancelButton.addEventListener('click', () => {
    ModalEditAppointmentOverlay.style.display = 'none';
});

cancelassignappbtn.addEventListener('click', () => {
    ModalAssignAppOverlay.style.display = 'none';
});

const editButtons = document.querySelectorAll('.EditAppointment-btn');

editButtons.forEach(button => {
    button.addEventListener('click', function () {
        const appointmentId = button.getAttribute('data-id');
	document.getElementById("appID").value = appointmentId;
        
	fetch(`/admin/get-appointment/${appointmentId}/`)
            .then(response => response.json())
            .then(data => {
                ModalEditAppointmentOverlay.style.display = "flex";

                document.getElementById('researchers-list').innerHTML = data.researchers.length ? data.researchers.map(researcher => researcher.name).join('<br>') : 'No researchers';
                document.getElementById('department-name').innerText = data.college || 'N/A';
                document.getElementById('transaction-code').innerText = data.transaction_id || 'N/A';
                document.getElementById('email-address').innerText = data.email || 'N/A';
                document.getElementById('release-date').value = data.release_date || '';
		document.getElementById('received-by').value = data.received_by || ''; 
            	document.getElementById('transactionCode').value = data.transaction_id || 'N/A';
	    })
            .catch(error => console.error('Error fetching appointment:', error));
    });
});



const assignButtons = document.querySelectorAll('.AssignAppointment-btn');
const reviewerContainer = document.getElementById("reviewer-list");
let manuscriptIDInput = document.getElementById('manuscriptID');

assignButtons.forEach(button => {
    button.addEventListener('click', function () {
        const collegeId = button.getAttribute('data-id');
        const manuscriptId = button.getAttribute('data-manuscript-id');

	ModalAssignAppOverlay.style.display = "flex";

        fetch(`/get_reviewers/${collegeId}/`)
            .then(response => response.json())
            .then(data => {
                if (!reviewerContainer) {
                    console.error("Reviewer container not found in the DOM.");
                    return;
                }

                if (data.success) {

                    reviewerContainer.innerHTML = "";

		data.reviewers.forEach((reviewer) => {
		    const row = document.createElement("tr");

		    const checkboxCell = document.createElement("td");
		    const checkbox = document.createElement("input");
		    checkbox.type = "checkbox";
		    checkbox.name = "reviewer_ids";
		    checkbox.value = reviewer.id;
		    checkboxCell.appendChild(checkbox);


		    const firstNameCell = document.createElement("td");
		    firstNameCell.textContent = reviewer.first_name;

		    const lastNameCell = document.createElement("td");
		    lastNameCell.textContent = reviewer.last_name;

		    const scheduleCell = document.createElement("td");
		    const select = document.createElement("select");

		    if (reviewer.schedules && reviewer.schedules.length > 0) {
			reviewer.schedules.forEach((schedule) => {
			    const option = document.createElement("option");
			    option.value = `${schedule.date},${schedule.start_time},${schedule.end_time},${schedule.type}`;
			    option.textContent = `${schedule.date || "N/A"}: ${schedule.start_time || "N/A"} - ${schedule.end_time || "N/A"} (${schedule.type || "N/A"})`;
			    select.appendChild(option);
			});
		    } else {
			const option = document.createElement("option");
			option.value = "N/A";
			option.textContent = "No schedules available";
			select.appendChild(option);
		    }

		    scheduleCell.appendChild(select);

		    row.appendChild(checkboxCell);
		    row.appendChild(firstNameCell);
		    row.appendChild(lastNameCell);
		    row.appendChild(scheduleCell);

		    reviewerContainer.appendChild(row);
		});

        	manuscriptIDInput.value = manuscriptId;

                } else {
                    console.error("Error fetching reviewers:", data.message);
                }
            })
            .catch(error => console.error("Error fetching reviewers:", error));
    });
});


