var modal_operacao = document.querySelector('.container-modal-operacao')
var modal_pesquisa = document.querySelector('.container-modal-pesquisa')
var selectChefe = document.getElementById('select-chefe')
var selectOperacao = document.getElementById('select-operacao')

function fechar_modal_operacao(){
    modal_operacao.style.display = 'none'
}

function abrir_pesquisa(target){
    modal_pesquisa.style.display = 'flex'
    // if (target.id == 'nome_suspeito'){
    //     modal_pesquisa.querySelector('label').textContent = 'Pesquisar suspeito:'
    //     modal_pesquisa.querySelector('input').name = 'input_pesquisa_suspeito:'
    //     console.log('suspeito')
    // } else if (target.id == 'nome_relator'){
    //     modal_pesquisa.querySelector('label').textContent = 'Pesquisar relator:'
    //     modal_pesquisa.querySelector('input').name = 'input_pesquisa_relator:'
    //     console.log('relator')
    // }
}

function fechar_pesquisa(){
    modal_pesquisa.style.display = 'none'
}


if (selectChefe.options[selectChefe.selectedIndex].value){
    modal_operacao.style.display = 'none'
    modal_pesquisa.style.display = 'flex'
}else{
    console.log("Nenhuma opção selecionada.");
}