var modal_operacao = document.querySelector('.container-modal-operacao')
var modal_pesquisa = document.querySelector('.container-modal-pesquisa')

window.onload = function() {
    var selectChefe = document.getElementById('select-chefe');
    var selectOperacao = document.getElementById('select-operacao');
    var btnOperacao = document.getElementById('btn-operacao');
    var check = selectChefe.options[selectChefe.selectedIndex].value && selectOperacao.options[selectOperacao.selectedIndex].value
  
    function checkInputs() {
        if(selectChefe.options[selectChefe.selectedIndex].value && selectOperacao.options[selectOperacao.selectedIndex].value){
            btnOperacao.disabled = false
        }else{
            btnOperacao.disabled = true
        }
    }
  
    selectChefe.addEventListener('input', checkInputs);
    selectOperacao.addEventListener('input', checkInputs);
    
    checkInputs();

    if(check){
        modal_operacao.style.display = 'none'
        modal_pesquisa.style.display = 'flex'
    }
}

function fechar_modal_operacao(){
    modal_operacao.style.display = 'none'
}

//////////////////////////////////////////////////////////////////////////

function abrir_pesquisa(tipo, pesquisa_anterior){
    modal_pesquisa.style.display = 'flex'
    modal_pesquisa.querySelector('input').value = ''
    var resultado = modal_pesquisa.querySelector('.resultados_pesquisa')
    if(pesquisa_anterior != tipo){
        resultado.style.display = 'none'
    }else{
        resultado.style.display = 'block'
    }
    if(tipo){
        modal_pesquisa.querySelector('label').textContent = 'Pesquisar '+tipo;
        modal_pesquisa.querySelector('#btn-pesquisa').value = tipo
        console.log(tipo)
    }

}

function fechar_pesquisa(){
    modal_pesquisa.style.display = 'none'
}

function adicionar_pessoa(target, tipo){
    info = target.previousElementSibling.querySelectorAll('span')
    campos = document.querySelector("#campos_"+tipo)

    info.forEach(function(item) {
        nome_campo = item.getAttribute('target')
        campo = campos.querySelector(`*[name*='${nome_campo}']`)
        if(nome_campo.includes('data') && item.textContent){
            var dateParts = item.textContent.trim().split('/')
            var formattedDate = `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`;
            campo.value = formattedDate
        }else{
            campo.value = item.textContent.trim()
        }
        // campo.disabled = true
    });

    mostrarInputsPessoa()
    scrollToElement(campos)
    modal_pesquisa.style.display = 'none'
}

function mostrarInputsPessoa(){
    var camposPessoas = document.querySelectorAll('.body_pessoa');
    camposPessoas.forEach(function(item){
        var inputs = item.querySelectorAll('input')
        inputs.forEach(function(input){
            if(input.value){
                item.parentElement.parentElement.classList.add('show')
            }
        })
     })
}

mostrarInputsPessoa()

function cadastrar_pessoa(tipo){
    var campos = document.querySelector("#campos_"+tipo)
    var body_accordion = campos.parentElement.parentElement

    inputs = campos.querySelectorAll(`*[name*='pessoa']`)
    inputs.forEach(function(item){
        item.value = ''
    })

    body_accordion.classList.add('show')
    modal_pesquisa.style.display = 'none'
    scrollToElement(body_accordion)
}

function scrollToElement(element) {
    if (element) element.scrollIntoView({ behavior: 'smooth' });
}

////////////////////////////////////////////////////////////////////////


document.addEventListener("DOMContentLoaded", function () {
    var cumprimentoMedidasCheckbox = document.getElementById("cumprimento_medidas");
    var camposCumprimentoMedidas = document.getElementById("camposCumprimentoMedidas");

    cumprimentoMedidasCheckbox.addEventListener("change", function () {
        camposCumprimentoMedidas.style.display = cumprimentoMedidasCheckbox.checked ? "block" : "none";
    });
    
    // Initial check when the page loads
    camposCumprimentoMedidas.style.display = cumprimentoMedidasCheckbox.checked ? "block" : "none";
});
