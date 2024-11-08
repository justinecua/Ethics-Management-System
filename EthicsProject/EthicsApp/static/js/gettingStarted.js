let CompleteProfilebtn = document.getElementById('Complete-Profile-btn');
let ModalCompleteProfileOverlay = document.getElementById('Modal-CompleteProfile-Overlay');
let AddThesisbtn = document.getElementById('AddThesis-btn');
let ModalThesisInfoOverlay = document.getElementById('Modal-ThesisInfo-Overlay');
let MTIContainer = document.getElementById('MTI-Container');

CompleteProfilebtn.addEventListener("click", function(){
  ModalCompleteProfileOverlay.style.display = "flex";
});

AddThesisbtn.addEventListener('click', function(){
  ModalThesisInfoOverlay.style.display = "flex";
})

document.addEventListener('click', function(event) {
    event.stopPropagation();
    if (event.target === ModalThesisInfoOverlay) {
        ModalThesisInfoOverlay.style.display = "none";
    }
});

