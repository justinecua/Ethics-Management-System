document.addEventListener("DOMContentLoaded", () => {
    console.log("Script loaded and DOM fully loaded.");
    
    const updateButtons = document.querySelectorAll(".UpdateCategory-btn");
    const modal = document.getElementById("updateCategoryModal");
    const closeModal = modal.querySelector(".close");
    const categoryIdInput = document.getElementById("categoryId");
    const categoryNameInput = document.getElementById("categoryName");

    console.log("Update buttons found:", updateButtons);

    // Handle the "Edit" button click
    updateButtons.forEach(button => {
        button.addEventListener("click", () => {
            console.log("Edit button clicked:", button);
            const categoryId = button.getAttribute("data-id");
            const categoryName = button.getAttribute("data-name");

            // Pre-fill the modal form fields
            categoryIdInput.value = categoryId;
            categoryNameInput.value = categoryName;

            // Display the modal
            modal.style.display = "block";
            console.log("Modal displayed with category ID:", categoryId);
        });
    });

    // Close the modal when the close button is clicked
    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Close the modal when clicking outside the modal content
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
