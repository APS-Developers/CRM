const table_filters = Array.from(document.getElementsByClassName("aps_table_filter"));
const table_modal = new bootstrap.Modal("#aps_table_modal",{
    keyboard:false
});
const filterIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-filter" viewBox="0 0 16 16">
<path d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5z"/>
</svg>`
table_filters.forEach((elem)=>{
    elem.innerHTML = elem.innerHTML+filterIcon;
    elem.addEventListener("click",()=>{
        table_modal.show(); 
    })
})