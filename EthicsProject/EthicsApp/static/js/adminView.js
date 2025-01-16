let ModalViewAppointmentOverlay = document.getElementById('Modal-View-Appointment-Overlay');
let backtolobby = document.getElementById('back-viewapp-btn');

// Close the modal when the back button is clicked
backtolobby.addEventListener('click', () => {
    ModalViewAppointmentOverlay.style.display = 'none';
});

// Handle view appointment button clicks
const viewButtons = document.querySelectorAll('.ViewAppointment-btn');

viewButtons.forEach(button => {
    button.addEventListener('click', function () {
        const appointmentId = button.getAttribute('data-id');
        console.log("Appointment ID:", appointmentId);

        // Fetch appointment data
        fetch(`/admin/get_view_appointment/${appointmentId}/`)
            .then(response => response.json())
            .then(data => {
                console.log("Fetched Data:", data);

                // Show the modal
                ModalViewAppointmentOverlay.style.display = "flex";

                // Populate thesis details
                document.getElementById('thesis-title').innerText = data.thesis_title || 'N/A';
                document.getElementById('thesis-description').innerText = data.thesis_description || 'N/A';
                document.getElementById('category-name').innerText = data.category_name || 'N/A';
                document.getElementById('type-of-study').innerText = data.type_of_study || 'N/A';
                document.getElementById('study-site').innerText = data.study_site || 'N/A';
                document.getElementById('email-address').innerText = data.email || 'N/A';
                document.getElementById('department-name').innerText = data.college || 'N/A';
                document.getElementById('institution-name').innerText = data.institution || 'N/A';
                document.getElementById('address-of-institution').innerText = data.address_of_institution || 'N/A';

                // Populate researchers list
                const researchersList = document.getElementById('researchers-list');
                researchersList.innerHTML = data.researchers.length > 0
                    ? data.researchers.map(researcher => `<p>${researcher.name} - Receipt No: ${researcher.receipt_no}</p>`).join('')
                    : 'No researchers';

                // Populate basic and supplementary requirements
                document.getElementById('basic-requirements').innerText = data.basic_requirements || 'No requirements';
                document.getElementById('supplementary-requirements').innerText = data.supplementary_requirements || 'No requirements';

                // Populate ethical risk questions & answers
                const ethicalRiskQuestions = document.getElementById('ethical-risk-questions');
                if (data.ethical_answers && data.ethical_answers.length > 0) {
                    ethicalRiskQuestions.innerHTML = data.ethical_answers.map(answer => {
                        return `
                            <div class="question">
                               ${answer.ethical_question}
                            </div>
                            <div class="answer">
                                <strong>:${answer.ethical_answer}</strong>
                            </div>
                        `;
                    }).join('');
                } else {
                    ethicalRiskQuestions.innerHTML = '<p>No ethical questions and answers available.</p>';
                }
            })
            .catch(error => console.error('Error fetching appointment:', error));
    });
});
