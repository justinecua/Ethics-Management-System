let AddCollegeBtn = document.getElementById('AddCollege-btn');
let ModalCollegeOverlay = document.getElementById('Modal-College-Overlay');
let COContainer = document.getElementById('CO-Continer');
let cancelCollege = document.getElementById('cancel-college');

AddCollegeBtn.addEventListener('click', function(event){
  event.stopPropagation();
  ModalCollegeOverlay.style.display = "flex";
})

cancelCollege.addEventListener('click', function(event){
  event.stopPropagation();
  ModalCollegeOverlay.style.display = "none";
})

document.addEventListener('click', function(event) {
    event.stopPropagation();
    if (event.target === ModalCollegeOverlay) {
        ModalCollegeOverlay.style.display = "none";
    }
});

var ListOfColleges = document.getElementById('ListOfColleges');
ListOfColleges.classList.add('active-btn');
ListOfColleges.style.backgroundColor = "#ffffff";



