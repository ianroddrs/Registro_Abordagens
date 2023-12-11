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
    }
}

function fechar_modal_operacao(){
    modal_operacao.style.display = 'none'
}

function fechar_pesquisa(){
    modal_pesquisa.style.display = 'none'
}

function abrir_pesquisa(tipo){
    modal_pesquisa.style.display = 'flex'
    document.getElementById('tipoEnvolvido').textContent = tipo
}

function atualizarContagem(item){
    var input = document.getElementById('qtd_pessoas')
    var qtd = item.parentElement.querySelectorAll('.accordion-item').length
    input.value = qtd
    return qtd
}

function adicionar_pessoa(target){
    var pessoas = document.getElementById('accordionCamposEnvolvidos').querySelectorAll('.accordion-item')
    var form = null
    var tipo_envolvio = document.getElementById('tipoEnvolvido').textContent
    var checkForm = true
    
    pessoas.forEach(function(item){
        var campos = item.querySelectorAll('input, select')
        campos.forEach(function(input){
            form = item
            if(input.value != ''){
                checkForm = false
            }
        })
    })

    if(checkForm==false){form = duplicar(form)}

    form.querySelector('.accordion-button').textContent = tipo_envolvio

    var info = target.previousElementSibling.querySelectorAll('span')
    info.forEach(function(item) {
        var nome_campo = item.getAttribute('target')
        var campo = form.querySelector(`*[name*='${nome_campo}']`)
        if(nome_campo.includes('data') && item.textContent){
            var dateParts = item.textContent.trim().split('/')
            var formattedDate = `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`;
            campo.value = formattedDate
        }else{
            campo.value = item.textContent.trim()
        }
        form.querySelector(`*[name*='atuacao']`).value = tipo_envolvio.trim().toUpperCase()
    });

    atualizarContagem(form)
    mostrarInputsPessoa(form)
}

function duplicar(form){
    var count = atualizarContagem(form)
    var formClone = form.cloneNode(true);
    formClone.querySelectorAll('input, select, label, div, button').forEach(function(field) {
        field.value = ''
        var oldId = field.getAttribute('id');
        var oldName = field.getAttribute('name');
        var oldFor = field.getAttribute('for');
        var oldTarget = field.getAttribute('data-bs-target');                       
        var oldControl = field.getAttribute('aria-controls');                       
        var oldParent = field.getAttribute('data-bs-parent');                       

        if (oldId) { field.setAttribute('id', oldId.replace(count.toString(), count + 1));}
        if (oldName) {field.setAttribute('name', oldName.replace(count.toString(), count + 1));}
        if (oldFor) {field.setAttribute('for', oldFor.replace(count.toString(), count + 1));}
        if (oldTarget) {field.setAttribute('data-bs-target', oldTarget.replace(count.toString(), count + 1));}
        if (oldControl) {field.setAttribute('aria-controls', oldControl.replace(count.toString(), count + 1));}
        if (oldParent) {field.setAttribute('data-bs-parent', oldParent.replace(count.toString(), count + 1));}
    });

    form.parentElement.appendChild(formClone)

    return formClone
}


function mostrarInputsPessoa(element){
    var envolvidos = element.parentElement.parentElement.parentElement
    var btnItem = element.querySelector('h2').querySelector('button')

    envolvidos.classList.add('show')
    btnItem.click()

    modal_pesquisa.style.display = 'none'
    scrollToElement(element)
}

function scrollToElement(element) {
    if (element) element.scrollIntoView({ behavior: 'smooth' });
}

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



function mostrarCumprimento(checkbox){
    checkbox.addEventListener("change", function () {
        camposCumprimentoMedidas.style.display = checkbox.checked ? "block" : "none";
    });
    
}





const user_input = $("#input_pesquisa")
const search_icon = $('#search-icon')
const resultado_div = $('.resultados_pesquisa')
const endpoint = '/cadastro/acoes/nro_ocorrencia/'
const delay_by_in_ms = 1000
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			// fade out the resultado_div, then:
			resultado_div.fadeTo('fast', 0, 'linear').promise().then(() => {
				// replace the HTML contents
				resultado_div.html(response['html_from_view'])
				// fade-in the div with new contents
				resultado_div.fadeTo('fast', 1, 'linear')
				// stop animating search icon
                search_icon.addClass('bi-search')
				search_icon.removeClass('spinner-border spinner-border-sm')
			})
		})
}


user_input.on('keyup', function () {
    const input_value = $(this).val();

	if (input_value.length > 3) {
		const request_parameters = {
			q: input_value
		}

        // start animating the search icon with the CSS class

        search_icon.removeClass('bi-search')
        search_icon.addClass('spinner-border spinner-border-sm')

        // if scheduled_function is NOT false, cancel the execution of the function
        if (scheduled_function) {
            clearTimeout(scheduled_function)
        }

        // setTimeout returns the ID of the function to be executed
        scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
    }
})


// Função para mostrar ou esconder campos com base na seleção do objeto apreendido
function toggleCampos() {
    var select_objeto = document.getElementById('id_apreensao1-objeto_apreendido')
    var objetoSelecionado = select_objeto.options[select_objeto.selectedIndex].value
    var campos_padrao = ["","DROGA", "MUNICAO", "RECURSO_NATURAL"];
    
    // Esconder todos os campos e labels relacionados a campos-form
    document.querySelectorAll('.campos-form').forEach(function(item){item.style.display = 'none'; item.previousElementSibling.style.display = 'none'})

    // Mostrar campos adicionais se não for uma droga, munição ou recurso natural
    if (campos_padrao.indexOf(objetoSelecionado) === -1) {
        document.querySelectorAll('.campos-form').forEach(function(item){item.style.display = 'block'; item.previousElementSibling.style.display = 'block'})
    }
}

// Chame a função inicialmente para configurar o estado correto dos campos
toggleCampos();

// Adicionar um ouvinte de evento de mudança ao campo "Objeto Apreendido"
document.getElementById('id_apreensao1-objeto_apreendido').addEventListener("change", function () {
    // Ao alterar o objeto apreendido, chame a função para atualizar a exibição dos campos
    toggleCampos();
});