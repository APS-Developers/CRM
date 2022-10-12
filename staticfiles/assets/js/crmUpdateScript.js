let HWDispatchedSerial = document.getElementById("HWDispatchedSerial");
let HWDispatched = document.getElementById("HWDispatched");
HWDispatchedSerial.value = HWDispatched.value;
let dataListElem = document.createElement("datalist");
dataListElem.setAttribute("class","d-None");
dataListElem.setAttribute("id","HWDispatchedSerialList");
dataListElem.innerHTML = document.getElementById("HWDispatched").innerHTML;
document.getElementById("HWDispatchedSerial").parentNode.appendChild(dataListElem);
HWDispatchedSerial.addEventListener("change",(e)=>{
    HWDispatched.value = e.target.value;
});