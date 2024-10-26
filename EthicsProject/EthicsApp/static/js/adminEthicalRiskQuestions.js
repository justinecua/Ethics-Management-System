document.addEventListener("DOMContentLoaded", function () {
    // Check that each element exists before adding event listeners
    let AddEthicalRiskQuestionsBtn = document.getElementById('AddEthicalRiskQuestions-btn');
    let ModalEthicalRiskQuestions = document.getElementById('Modal-EthicalRiskQuestions-Overlay');
    let cancelEthicalQuestions = document.getElementById('cancel-ethicalquestion');

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
