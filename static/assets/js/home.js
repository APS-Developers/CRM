const images = Array.from(document.getElementsByClassName("image_wrapper"));
const image_count = images.length;
const scrollStops = images.map(image => image.offsetTop);
let timeout = null;
document.addEventListener("scroll",(e)=>{
    if(timeout){
        clearTimeout(timeout);
    }
    let currScroll = window.scrollY;
    setTimeout(()=>{
        for(let i=0;i<scrollStops.length;i++){
            if(currScroll>=scrollStops[i]+20){
                if(i+1<scrollStops.length){
                    if(Math.abs(currScroll-scrollStops[i])>Math.abs(currScroll-scrollStops[i+1])){
                        window.scrollTo({'left':0,'top':scrollStops[i+1],behavior:'instant'});
                    }
                    else{
                        window.scrollTo({'left':0,'top':scrollStops[i],behavior:'instant'});
                    }
                }
            }
        }
    },500);
});
setInterval(()=>{
    let scrollAmount = Math.round(window.scrollY+images[0].getBoundingClientRect().height);
    if(scrollAmount>=document.getElementById("aps_main_carousel").scrollHeight){
        scrollAmount=0;
    }
    window.scrollTo({
        top:scrollAmount,
        left:0, 
        behavior:"instant"
    });
},5000)