var docking_date = document.getElementById('dockingDate');
var reminder = document.registerForm.reminderType;
const daysType = document.getElementById('daysType');
const dateType = document.getElementById('dateType');

today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();

today_date = yyyy + '-' + mm + '-' + dd;
if(docking_date.value == ''){
    docking_date.value = today_date;
}

check()

for(var i = 0; i < reminder.length; i++){
    reminder[i].addEventListener('change', check)
}

function check(){
    if (reminder.value === 'day'){
        daysType.style.display = 'block';
        dateType.style.display = 'none';
    }else{
        dateType.style.display = 'block';
        daysType.style.display = 'none';
    }
}

formInputs = document.registerForm;
for(var i = 0; i < formInputs.length; i++){
    formInputs[i].addEventListener('change', (event)=>{
        if(event.target.value === '' && event.target.name != 'reference'){
            event.target.classList.add('is-invalid');
        }else{
            event.target.classList.remove('is-invalid');
        };
        validateForm();
    });
}; 

function validateForm(){
    var formInputs = document.registerForm;
    if(formInputs.name.value == '' || formInputs.address.value == ''
    || formInputs.phone.value == '' || formInputs.email.value == ''
    || formInputs.dockingDate.value == '' || 
    (formInputs.reminderDate.value == '' && formInputs.reminderDays.value == '')){
        formInputs.registerBtn.disabled = true;
    }else{
        formInputs.registerBtn.disabled = false;
    }
}