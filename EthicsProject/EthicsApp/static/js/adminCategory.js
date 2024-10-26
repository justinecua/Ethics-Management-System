let AddCategoryBtn = document.getElementById('AddCategory-btn');
let ModalCategoryOverlay = document.getElementById('Modal-Category-Overlay');
let COContainer = document.getElementById('CO-Continer');
let cancelCategory = document.getElementById('cancel-category');

AddCategoryBtn.addEventListener('click', function(event){
  event.stopPropagation();
  ModalCategoryOverlay.style.display = "flex";
})

cancelCategory.addEventListener('click', function(event){
  event.stopPropagation();
  ModalCategoryOverlay.style.display = "none";
})

document.addEventListener('click', function(event) {
    event.stopPropagation();
    if (event.target === ModalCategoryOverlay) {
        ModalCategoryOverlay.style.display = "none";
    }
});





