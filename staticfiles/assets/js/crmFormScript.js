document.querySelectorAll(".crm_form fieldset").forEach((elem) => {
    try {
        let lbl = elem.querySelector("label");
        let ip = lbl.nextElementSibling;
        if (ip.hasAttribute("required") && lbl.innerHTML.indexOf("*") == -1) {
            lbl.innerHTML += "<span class='text-danger'> *</span>";
        }
    } catch {}
})

function debounce(func, timeout = 300) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, args);
        }, timeout);
    };
}

let organization = document.getElementById("aps_crm_Organisation");
let customer_name = document.getElementById("aps_crm_customer_name");
let email = document.getElementById("aps_crm_customer_email");
let phone = document.getElementById("aps_crm_customer_phone");
let aps_crm_customer_id = document.getElementById("aps_crm_customer_id");
customer_name.addEventListener("input",()=>{
    debounce(()=>{
        fetch("/customerDetailsAutofill?"+new URLSearchParams({"name":customer_name.value,"org":organization.value})).then(res=>res.json()).then(data=>{
            if(data.email){
                email.value = data.email;
                email.setAttribute("readonly",true);
                aps_crm_customer_id.value = data.id;
            }
            else{
                email.value="";
                email.removeAttribute("readonly");
                aps_crm_customer_id.value="";
            }
            if(data.contactNo){ 
                phone.value = data.contactNo;
                phone.setAttribute("readonly",true);
            }
            else{
                phone.value = "";
                phone.removeAttribute("readonly");
            }
        })
    })();
});

// Code for serial search
const serial_search_form = document.getElementById("aps_crm_serial_search");
const crm_input_form = document.getElementById("aps_crm_input_form");
serial_search_form.addEventListener("submit", (e) => {
    e.preventDefault();
    toggleLoader();
    const serial = serial_search_form.querySelector("input[name='serial']").value;
    const url = serial_search_form.getAttribute("action")+'?'+new URLSearchParams({serial:serial}).toString();
    const method = serial_search_form.getAttribute("method");
    fetch(url, {method:method}).then((res)=>res.json()).then((data)=>{
        if(data.error){
            throw Error(data.error)
        }
        serial_search_form.classList.toggle("d-none");
        crm_input_form.classList.toggle("d-none");
        fillForm(data);
    }).catch((err)=>{
        console.log(err);
        alert("Error while Searching serial");
    }).finally(()=>{
        toggleLoader();
    })
})

function fillForm(data){
    document.getElementById("aps_crm_"+"SNo").value = data.SNo;
    document.getElementById("aps_crm_"+"Make").value = data.Make;
    document.getElementById("aps_crm_"+"PartCode").value = data.PartCode;
    document.getElementById("aps_crm_"+"Item").value = data.Item;
    document.getElementById("aps_crm_"+"Item_dispatched_Date").value = data.Item_dispatched_Date;
    document.getElementById("aps_crm_"+"Organisation").value = data.Organisation;
    document.getElementById("aps_crm_"+"organisation_id").value = data.OrganisationId;
}