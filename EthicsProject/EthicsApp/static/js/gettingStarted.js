let CompleteProfilebtn = document.getElementById('Complete-Profile-btn');
let ModalCompleteProfileOverlay = document.getElementById('Modal-CompleteProfile-Overlay');
let AddThesisbtn = document.getElementById('AddThesis-btn');
let ModalThesisInfoOverlay = document.getElementById('Modal-ThesisInfo-Overlay');
let MTIContainer = document.getElementById('MTI-Container');
let AddMembersbtn = document.getElementById('AddMembers-btn');
let ModalThesisMembersOverlay = document.getElementById('Modal-ThesisMembers-Overlay');
let MemberAddbtn = document.getElementById('MemberAdd-btn');
let MemberInputContainer = document.querySelector('.MemberInputContainer'); 

if (CompleteProfilebtn) {
  CompleteProfilebtn.addEventListener("click", function(){
    ModalCompleteProfileOverlay.style.display = "flex";
  });
}

if (AddThesisbtn) {
  AddThesisbtn.addEventListener('click', function(){
    ModalThesisInfoOverlay.style.display = "flex";
  });
}

if (AddMembersbtn) {
  AddMembersbtn.addEventListener('click', function(){
    ModalThesisMembersOverlay.style.display = "flex";
  });
}

if (MemberAddbtn) {
  MemberAddbtn.addEventListener('click', function(){
    let ContainerMember = document.createElement('div');
    let FNLabel = document.createElement('label');
    let FNInput = document.createElement('input');

    let LNLabel = document.createElement('label');
    let LNInput = document.createElement('input');

    let RLabel = document.createElement('label');
    let RInput = document.createElement('input');
    
    let ELabel = document.createElement('label');
    let EInput = document.createElement('input');

    let MTICMM1 = document.createElement('div');
    MTICMM1.className = "MTICMM1";
    let MTICMM2 = document.createElement('div');
    MTICMM2.className = "MTICMM2";
    let MTICMM3 = document.createElement('div');
    MTICMM3.className = "MTICMM3";
    let MTICMM4 = document.createElement('div');
    MTICMM4.className = "MTICMM4";
    ContainerMember.className = "ContainerMember";
    
    FNLabel.innerHTML = "First Name";
    FNInput.placeholder = "Input First Name";
    FNInput.name = "firstnames";  
    LNLabel.innerHTML = "Last Name";
    LNInput.placeholder = "Input Last Name";
    LNInput.name = "lastnames";    
    RLabel.innerHTML = "Receipt No.";
    RInput.placeholder = "Input receipt no.";
    RInput.name = "receipt_nos";
    ELabel.innerHTML = "Email";
    EInput.placeholder = "Input email address";
    EInput.name = "emails";       

    MTICMM1.append(FNLabel, FNInput);
    MTICMM2.append(LNLabel, LNInput);
    MTICMM3.append(RLabel, RInput);
    MTICMM4.append(ELabel, EInput);

    ContainerMember.append(MTICMM1, MTICMM2, MTICMM3, MTICMM4);
    MemberInputContainer.append(ContainerMember);
  });
}

document.addEventListener('click', function(event) {
    event.stopPropagation();
    if (event.target === ModalThesisInfoOverlay) {
        ModalThesisInfoOverlay.style.display = "none";
    }

    if (event.target === ModalCompleteProfileOverlay) {
        ModalCompleteProfileOverlay.style.display = "none";
    }

    if (event.target === ModalThesisMembersOverlay) {
        ModalThesisMembersOverlay.style.display = "none";
    }
});

