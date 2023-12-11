const inputs = document.querySelectorAll('input');

function mascara(obj, fun) {
    obj.addEventListener("keyup", function() {
        var cursorPosition = obj.selectionStart;
        obj.value = fun(obj.value);
        obj.selectionStart = obj.selectionEnd = cursorPosition;
    });
 }
 

function mboletim(v) {
    v = v.replace(/\D/g, "");
    v = v.replace(/(\d)(\d{1})$/, "$1-$2");
    v = v.replace(/^(\d{5,9})(\d{6})/g, "$1.$2");
    v = v.replace(/^(\d{1,5})(\d{4})/g, "$1/$2");
    return v;
}

function mnumber(v) {
    v = v.replace(/\D/g, "");
    return v;
}

function mtext(v) {
    v = v.replace(/[^a-zA-ZÀ-ú0-9\s]/g, "");
    v = v.toUpperCase();
    v = v.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    v = v.replace(/Ç/g, "C");
    return v;
}

inputs.forEach(function(input) {
    if (input.type != 'password' && input.type != 'date' && input.type != 'number'){
        const inputType = input.getAttribute("mask");
        var maskFunction 
        if(inputType === "bop"){
            maskFunction = mboletim;
        }else if(inputType === "number"){
            maskFunction = mnumber;
        }else{
            maskFunction = mtext;
        }
        mascara(input, maskFunction);
    }
});
