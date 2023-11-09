var modal_operacao = document.querySelector('.container-modal-operacao')
var modal_pesquisa = document.querySelector('.container-modal-pesquisa')
var selectChefe = document.getElementById('select-chefe')
var selectOperacao = document.getElementById('select-operacao')

function fechar_modal_operacao(){
    modal_operacao.style.display = 'none'
}

function abrir_pesquisa(tipo){
    modal_pesquisa.style.display = 'flex'
    modal_pesquisa.querySelector('input').value = ''
    var resultado = modal_pesquisa.querySelector('.resultados_pesquisa')
    if(resultado){
        resultado.parentElement.removeChild(resultado)
    }
    if (tipo == 'suspeito'){
        modal_pesquisa.querySelector('label').textContent = 'Pesquisar suspeito:'
        modal_pesquisa.querySelector('#btn-pesquisa').value = 'suspeito'
        console.log('suspeito')
    } else if (tipo == "relator"){
        modal_pesquisa.querySelector('label').textContent = 'Pesquisar relator:'
        modal_pesquisa.querySelector('#btn-pesquisa').value = 'relator'
        console.log('relator')
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
        campo.value = item.textContent.trim()
    });

    modal_pesquisa.style.display = 'none'
}


if(selectChefe.options[selectChefe.selectedIndex].value && selectOperacao.options[selectOperacao.selectedIndex].value){
    modal_operacao.style.display = 'none'
    modal_pesquisa.style.display = 'flex'
}else{
    console.log("Nenhuma opção selecionada.");
}