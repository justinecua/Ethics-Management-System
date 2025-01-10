let StudentsAccounts = document.getElementById('Students-Accounts');
let ReviewerAccounts = document.getElementById('Reviewer-Accounts');
let AdminAccounts = document.getElementById('AdminAccounts');
let StudentAccArea = document.getElementById('StudentAcc-Area');
let ReviewerAccArea = document.getElementById('ReviewerAcc-Area');
let AdminAccArea = document.getElementById('AdminAcc-Area');
let InviteAccbtn = document.getElementById('InviteAcc-btn');
let ModalAddAccountOverlay = document.getElementById('Modal-AddAccount-Overlay');
let AddAccountCancel = document.getElementById('AddAccount-Cancel');

StudentsAccounts.classList.add('active-btn');
StudentsAccounts.style.backgroundColor = "#ffffff";

var areas = document.querySelectorAll('.ACT-Left button');
areas.forEach(function(area) {
    area.addEventListener('click', function() {
        areas.forEach(function(areabtn) {
            areabtn.classList.remove('active-btn');
            areabtn.style.backgroundColor = "";
        });

        this.classList.add('active-btn');
        this.style.backgroundColor = '#ffffff';

        if (this.id === 'Students-Accounts') {
            StudentAccArea.style.display = "flex";
            ReviewerAccArea.style.display = "none";
            AdminAccArea.style.display = "none";
        } else if (this.id === 'Reviewer-Accounts') {
            StudentAccArea.style.display = "none";
            ReviewerAccArea.style.display = "flex";
            AdminAccArea.style.display = "none";
        } else if (this.id === 'Admin-Accounts') {
            StudentAccArea.style.display = "none";
            ReviewerAccArea.style.display = "none";
            AdminAccArea.style.display = "flex";
        }
    });
});

InviteAccbtn.addEventListener('click', function(event){
  event.stopPropagation();
  ModalAddAccountOverlay.style.display = "flex";
})

AddAccountCancel.addEventListener('click', function(event){
  event.stopPropagation();
  ModalAddAccountOverlay.style.dislay = "none";
})

document.addEventListener('click', function(event) {
    event.stopPropagation();
    if (event.target === ModalAddAccountOverlay) {
        ModalAddAccountOverlay.style.display = "none";
    }
});


