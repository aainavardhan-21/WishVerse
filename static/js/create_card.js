const input=document.getElementById("coverImage");

const preview=document.getElementById("previewImage");

if(input){

input.addEventListener("change",function(){

const file=this.files[0];

if(file){

preview.src=URL.createObjectURL(file);

preview.style.display="block";

}

});

}