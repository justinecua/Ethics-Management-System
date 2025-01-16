document.addEventListener("DOMContentLoaded", function () {
    // Check that each element exists before adding event listeners
    let AddEthicalRiskQuestionsBtn = document.getElementById('AddEthicalRiskQuestions-btn');
    let ModalEthicalRiskQuestions = document.getElementById('Modal-EthicalRiskQuestions-Overlay');
    let cancelEthicalQuestions = document.getElementById('cancel-ethicalquestion');
    let editButtons = document.querySelectorAll('.TableEdit-Btn');
    let editModal = document.getElementById('Modal-EditEthicalRiskQuestions-Overlay');
    let cancelEditBtn = document.getElementById('cancel-edit-ethicalquestion');
    let editQuestionIdInput = document.getElementById('edit-question-id');
    let editQuestionTextArea = document.getElementById('edit-ethical-questions');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            let questionId = this.getAttribute('data-id');
            let questionText = this.getAttribute('data-question');

            editQuestionIdInput.value = questionId;
            editQuestionTextArea.value = questionText;

            editModal.style.display = "flex";
        });
    });

    // Close Edit Modal
    if (cancelEditBtn) {
        cancelEditBtn.addEventListener('click', function () {
            editModal.style.display = "none";
        });
    }

    // Close Edit Modal on Overlay Click
    if (editModal) {
        document.addEventListener('click', function (event) {
            if (event.target === editModal) {
                editModal.style.display = "none";
            }
        });
    }

    // Only add event listeners if elements are found
    if (AddEthicalRiskQuestionsBtn) {
        AddEthicalRiskQuestionsBtn.addEventListener('click', function (event) {
            event.stopPropagation();
            ModalEthicalRiskQuestions.style.display = "flex";
        });
    }

    if (cancelEthicalQuestions) {
        cancelEthicalQuestions.addEventListener('click', function (event) {
            event.stopPropagation();
            ModalEthicalRiskQuestions.style.display = "none";
        });
    }

    // Close the modal when clicking outside of the modal content
    if (ModalEthicalRiskQuestions) {
        document.addEventListener('click', function (event) {
            if (event.target === ModalEthicalRiskQuestions) {
                ModalEthicalRiskQuestions.style.display = "none";
            }
        });
    }
});
