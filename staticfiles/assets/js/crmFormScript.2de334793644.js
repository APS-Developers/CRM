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

try {

    let organization = document.getElementById("aps_crm_Organisation");
    let customer_name = document.getElementById("aps_crm_customer_name");
    let email = document.getElementById("aps_crm_customer_email");
    let phone = document.getElementById("aps_crm_customer_phone");
    let aps_crm_customer_id = document.getElementById("aps_crm_customer_id");
    customer_name.addEventListener("input", () => {
        debounce(() => {
            fetch("/customerDetailsAutofill?" + new URLSearchParams({
                "name": customer_name.value,
                "org": organization.value
            })).then(res => res.json()).then(data => {
                if (data.email) {
                    email.value = data.email;
                    email.setAttribute("readonly", true);
                    aps_crm_customer_id.value = data.id;
                } else {
                    email.value = "";
                    email.removeAttribute("readonly");
                    aps_crm_customer_id.value = "";
                }
                if (data.contactNo) {
                    phone.value = data.contactNo;
                    phone.setAttribute("readonly", true);
                } else {
                    phone.value = "";
                    phone.removeAttribute("readonly");
                }
            })
        })();
    });
} catch (e) {
    console.log(e);
}
