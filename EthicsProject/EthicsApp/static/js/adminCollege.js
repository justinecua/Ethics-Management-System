document.addEventListener("DOMContentLoaded", function () {
  // Check that each element exists before adding event listeners
  const addCollegeBtn = document.getElementById('AddCollege-btn');
  const modalCollegeOverlay = document.getElementById('Modal-College-Overlay');
  const cancelCollege = document.getElementById('cancel-college');
  const editButtons = document.querySelectorAll('.TableEdit-Btn');
  const editModal = document.getElementById('Modal-EditCollege-Overlay');
  const editCancelBtn = document.getElementById('cancel-edit-college');
  const editCollegeId = document.getElementById('edit-college-id');
  const editCollegeInitial = document.getElementById('edit-college-initial');
  const editCollegeName = document.getElementById('edit-college-name');
  const deleteButtons = document.querySelectorAll('.TableDelete-Btn');
  const deleteModal = document.getElementById('Modal-DeleteCollege-Overlay');
  const deleteCancelBtn = document.getElementById('cancel-delete-college');
  const deleteCollegeId = document.getElementById('delete-college-id');

  // Add College Modal Logic
  if (addCollegeBtn && modalCollegeOverlay) {
      addCollegeBtn.addEventListener('click', function (event) {
          event.stopPropagation();
          modalCollegeOverlay.style.display = "flex";
      });

      if (cancelCollege) {
          cancelCollege.addEventListener('click', function (event) {
              event.stopPropagation();
              modalCollegeOverlay.style.display = "none";
          });
      }

      document.addEventListener('click', function (event) {
          if (event.target === modalCollegeOverlay) {
              modalCollegeOverlay.style.display = "none";
          }
      });
  }

  // Edit College Modal Logic
  // Edit College Modal Logic
editButtons.forEach(button => {
  button.addEventListener('click', function () {
      const collegeRow = this.closest('tr');
      if (!collegeRow) {
          console.error("College row not found for this button.");
          return;
      }

      const collegeId = collegeRow.dataset.collegeId;
      const collegeInitial = collegeRow.querySelector('td:nth-child(1)')?.innerText || '';
      const collegeName = collegeRow.querySelector('td:nth-child(2)')?.innerText || '';

      if (editCollegeId && editCollegeInitial && editCollegeName) {
          editCollegeId.value = collegeId || '';
          editCollegeInitial.value = collegeInitial;
          editCollegeName.value = collegeName;

          const editForm = editModal.querySelector('form');
          if (editForm) {
              editForm.action = `/adminEditCollege/${collegeId}/`;
              editForm.addEventListener('submit', function (event) {
                  event.preventDefault(); // Prevent form from reloading page
                  const formData = new FormData(editForm);

                  fetch(editForm.action, {
                      method: "POST",
                      body: formData,
                      headers: {
                          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                      },
                  })
                  .then(response => {
                      if (response.ok) {
                          alert("College updated successfully!");
                          window.location.reload(); // Reload the page to reflect updates
                      } else {
                          alert("Failed to update college. Please try again.");
                      }
                  })
                  .catch(error => {
                      console.error("Error submitting form:", error);
                      alert("An error occurred. Please try again.");
                  });
              });
          }

          editModal.style.display = "flex";
      } else {
          console.error("Edit modal inputs not found");
      }
  });
});


  // Close Edit Modal
  if (editCancelBtn) {
      editCancelBtn.addEventListener('click', function () {
          if (editModal) {
              editModal.style.display = "none";
          }
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

  // Delete College Modal Logic
  deleteButtons.forEach(button => {
      button.addEventListener('click', function () {
          const collegeRow = this.closest('tr');
          if (!collegeRow) {
              console.error("College row not found for this button.");
              return;
          }

          const collegeId = collegeRow.dataset.collegeId;

          if (deleteCollegeId) {
              deleteCollegeId.value = collegeId || '';
              if (deleteModal) {
                  deleteModal.style.display = "flex";
              }
          } else {
              console.error("Delete modal input not found");
          }
      });
  });

  // Close Delete Modal
  if (deleteCancelBtn) {
      deleteCancelBtn.addEventListener('click', function () {
          if (deleteModal) {
              deleteModal.style.display = "none";
          }
      });
  }

  // Close Delete Modal on Overlay Click
  if (deleteModal) {
      document.addEventListener('click', function (event) {
          if (event.target === deleteModal) {
              deleteModal.style.display = "none";
          }
      });
  }

  // Highlight Active Menu Item
  const listOfColleges = document.getElementById('ListOfColleges');
  if (listOfColleges) {
      listOfColleges.classList.add('active-btn');
      listOfColleges.style.backgroundColor = "#ffffff";
  }
});
