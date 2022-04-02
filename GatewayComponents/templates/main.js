var navs=document.getElementById("navbarNav").getElementsByClassName("nav-link");
for(var i=0;i<navs.length;i++){
    navs[i].addEventListener("click",f(){
        document.getElementsByClassName("active")[0].className=document.getElementsByClassName("active")[0].className.replace(" active","");

    });
}``