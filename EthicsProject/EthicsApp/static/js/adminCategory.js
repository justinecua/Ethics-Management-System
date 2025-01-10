let AddCategoryBtn = document.getElementById('AddCategory-btn');
let CategoryBTN = document.getElementById('Category-btn');
let CategoryArea = document.getElementById('Category-area');

let AddStudTypeBtn = document.getElementById('AddStudType-btn');
let TypeStudyBTN = document.getElementById('TypeStudy-btn');
let StudTypeArea = document.getElementById('StudType-area');

let AddBRBtn = document.getElementById('AddBR-btn');
let BrBTN = document.getElementById('Br-btn');
let BRArea = document.getElementById('BR-area');

let AddSDBtn = document.getElementById('AddSD-btn');
let SdBTN = document.getElementById('Sd-btn');
let SDArea = document.getElementById('SD-area');

// Modal References
let ModalCategoryOverlay = document.getElementById('Modal-Category-Overlay');
let cancelCategory = document.getElementById('cancel-category');

let ModalStudyOverlay = document.getElementById('Modal-Study-Overlay');
let cancelStudy = document.getElementById('cancel-study');

let ModalBasicOverlay = document.getElementById('Modal-Basic-Overlay');
let cancelBasic = document.getElementById('cancel-basic');


let ModalSDOverlay = document.getElementById('Modal-SD-Overlay');
let cancelSD = document.getElementById('cancel-sd');

CategoryBTN.classList.add('active-btn');
CategoryBTN.style.backgroundColor = "#ffffff";


function displayOnly(selectedArea, addButton) {
   
    CategoryArea.style.display = "none";
    StudTypeArea.style.display = "none";
    BRArea.style.display = "none";
    SDArea.style.display = "none";
    
    AddCategoryBtn.style.display = "none";
    AddStudTypeBtn.style.display = "none";
    AddBRBtn.style.display = "none";
    AddSDBtn.style.display = "none";

   
    selectedArea.style.display = "flex";
    addButton.style.display = "inline-block";
}


function setActiveButton(button) {
   
    [CategoryBTN, TypeStudyBTN, BrBTN, SdBTN].forEach(btn => {
        btn.classList.remove('active-btn');
        btn.style.backgroundColor = "";
    });
    
    button.classList.add('active-btn');
    button.style.backgroundColor = "#ffffff";
}


CategoryBTN.addEventListener('click', function() {
    displayOnly(CategoryArea, AddCategoryBtn);
    setActiveButton(this);
});
TypeStudyBTN.addEventListener('click', function() {
    displayOnly(StudTypeArea, AddStudTypeBtn);
    setActiveButton(this);
});
BrBTN.addEventListener('click', function() {
    displayOnly(BRArea, AddBRBtn);
    setActiveButton(this);
});
SdBTN.addEventListener('click', function() {
    displayOnly(SDArea, AddSDBtn);
    setActiveButton(this);
});

// Modal open and close logic for CATEGORY
AddCategoryBtn.addEventListener('click', function(event) {
    event.stopPropagation();
    ModalCategoryOverlay.style.display = "flex";
});

cancelCategory.addEventListener('click', function(event) {
    event.stopPropagation();
    ModalCategoryOverlay.style.display = "none";
});


document.addEventListener('click', function(event) {
    if (event.target === ModalCategoryOverlay) {
        ModalCategoryOverlay.style.display = "none";
    }
});

// Modal open and close logic for TYPE OF STUDY
AddStudTypeBtn.addEventListener('click', function(event) {
    event.stopPropagation();
    ModalStudyOverlay.style.display = "flex";
});

cancelStudy.addEventListener('click', function(event) {
    event.stopPropagation();
    ModalStudyOverlay.style.display = "none";
});


document.addEventListener('click', function(event) {
    if (event.target === ModalStudyOverlay) {
        ModalStudyOverlay.style.display = "none";
    }
});


// Modal open and close logic for Basic Req
AddBRBtn.addEventListener('click', function(event) {
    event.stopPropagation();
    ModalBasicOverlay.style.display = "flex";
});

cancelBasic.addEventListener('click', function(event) {
    event.stopPropagation();
    ModalBasicOverlay.style.display = "none";
});


document.addEventListener('click', function(event) {
    if (event.target === ModalBasicOverlay) {
        ModalBasicOverlay.style.display = "none";
    }
});


// Modal open and close logic for Supplementary Requirements
AddSDBtn.addEventListener('click', function(event) {
    event.stopPropagation();
    ModalSDOverlay.style.display = "flex";
});

cancelSD.addEventListener('click', function(event) {
    event.stopPropagation();
    ModalSDOverlay.style.display = "none";
});


document.addEventListener('click', function(event) {
    if (event.target === ModalSDOverlay) {
        ModalSDOverlay.style.display = "none";
    }
});