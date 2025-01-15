let ModalEditAppointmentOverlay = document.getElementById('Modal-Edit-Appointment-Overlay');
let cancelButton = document.getElementById('cancel-editapp-btn');

cancelButton.addEventListener('click', () => {
    ModalEditAppointmentOverlay.style.display = 'none';
});

const editButtons = document.querySelectorAll('.EditAppointment-btn');

editButtons.forEach(button => {
    button.addEventListener('click', function () {
        const appointmentId = button.getAttribute('data-id');

        fetch(`/admin/get-appointment/${appointmentId}/`)
            .then(response => response.json())
            .then(data => {
                ModalEditAppointmentOverlay.style.display = "flex";

                document.getElementById('researchers-list').innerHTML = data.researchers.length ? data.researchers.map(researcher => researcher.name).join('<br>') : 'No researchers';
                document.getElementById('department-name').innerText = data.college || 'N/A';
                document.getElementById('transaction-code').innerText = data.transaction_id || 'N/A';
                document.getElementById('email-address').innerText = data.email || 'N/A';
                document.getElementById('release-date').value = data.release_date || '';  // If you want to set the value of the date
                document.getElementById('received-by').value = data.received_by || '';  // If you want to set the value of the text input
            })
            .catch(error => console.error('Error fetching appointment:', error));
    });
});
