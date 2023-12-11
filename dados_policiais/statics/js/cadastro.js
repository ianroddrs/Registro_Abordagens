function validarFormulario() {
    const formulario = document.querySelector('form')
    
    var x = true
    var pessoa = true
    var apreensao = true

    var msg = "<strong>Campos obrigatórios não preenchidos.</strong>"
    var list = ""
    
    document.querySelectorAll('select, input').forEach(function(item){
        if (!item.checkValidity()) {
            item.classList.add('warning-form')
            x = false;
            if(item.name.includes('pessoa') && pessoa ){
                list += '<li>Um ou mais campos de <span class="text-danger">Envolvidos</span> não foram preenchidos</li>'
                pessoa = false
            }else if(item.name.includes('apreensao') && apreensao){
                list += '<li>Um ou mais campos de <span class="text-danger">Apreensão</span> não foram preenchidos</li>'
                apreensao = false
            }else if(!item.name.includes('apreensao') && !item.name.includes('pessoa')){
                var nomeItem = document.querySelector(`label[for=${item.id}]`).textContent.replace(':','')
                list += `<li>O campo <span class='text-danger'>${nomeItem}</span> não foi preenchido</li>`
            }
        }
    })

    msg += '<ul class="text-start mt-2">'+ list +'</ul>'
    
    if(x){
        formulario.submit()
    }else{
        var info = document.querySelector('.container-modal-info')
        info.style.display = 'flex'
        info.querySelector('#text').innerHTML = msg
    }
}


function requiredMark(){
    document.querySelectorAll('input, select').forEach(function(item){
        if(item.getAttribute('required') != null){
            if(!(item.previousElementSibling && item.previousElementSibling.tagName.toLowerCase() === 'span' && item.previousElementSibling.classList.contains('required') || item.classList.contains('d-none'))){
                var newSpan = document.createElement('span');
                newSpan.className = 'required';
                newSpan.textContent = '*';
     
                var parentElement = item.parentNode
     
                parentElement.insertBefore(newSpan, item)
            }
        }
    
        item.addEventListener('keyup', function () {
            item.classList.remove('warning-form')
        })
       
        item.addEventListener('change', function () {
            item.classList.remove('warning-form')
        })
    })
}

requiredMark()

var modal_operacao = document.querySelector('.container-modal-operacao')
var modal_pesquisa = document.querySelector('.container-modal-pesquisa')


function abrir_pesquisa(tipo){
    modal_pesquisa.style.display = 'flex'
    document.getElementById('tipoEnvolvido').textContent = tipo
    document.getElementById('btn-cadastrar-pessoa').setAttribute('onclick', `cadastrar_pessoa('${tipo}')`)
}

function atualizarContagem(){
    var input = document.querySelectorAll('.qtd_fomrs')
    input.forEach(function(item){
        qtd = item.previousElementSibling.querySelectorAll('.accordion-item').length
        item.value = qtd
    })
}

function verificarVazio(item){
    var vazio = true
    var campos = item.querySelectorAll('input, select')
        item.querySelector('h2').querySelector('button').classList.add('collapsed')
        item.querySelector('h2').querySelector('button').setAttribute('aria-expanded','false')
        item.querySelector('h2').parentElement.nextElementSibling.classList.remove('show')
        campos.forEach(function(input){
            if(input.value != ''  && (!input.name.includes('objeto_apreendido') &&  !input.name.includes('atuacao') && !input.name.includes('pj'))){
                vazio = false
            }
        })
    return vazio
}

function adicionarApreensao(opt){
    var apreensoes = Array.from(document.getElementById('accordionCamposApreensao').querySelectorAll('.accordion-item'))
    var form = null
    var tipo_apreensao = opt.textContent.trim()
    var checkForm = true

    apreensoes.every(item =>{
        form = item
        checkForm = verificarVazio(item)
        if(checkForm){
            return false;
        }else{
            return true;
        }
    })

    if(checkForm==false){ form = duplicar(form)}

    form.querySelector('.accordion-button').textContent = tipo_apreensao
    form.querySelector(`*[name*='objeto_apreendido']`).value = tipo_apreensao.trim().toUpperCase()

    if(tipo_apreensao == 'celular'){
        var lista_campos = ['tipo_objeto','especie_modelo','und_medida','nro_identificador', 'nro_identificador2']
        
        form.querySelector('label[for*="tipo_objeto"]').textContent = "Marca" 
        form.querySelector('label[for*="nro_identificador"]').textContent = "Nº IMEI¹"
        form.querySelector('label[for*="nro_identificador2"]').textContent = "Nº IMEI²"
        form.querySelector('label[for*="especie_modelo"]').textContent = "Modelo"

        
        form.querySelector('select[name*="und_medida"]').value = 'UND'
        form.querySelector('input[name*="tipo_nro_identificador"]').value = "IMEI"
        form.querySelector('input[name*="tipo_nro_identificador2"]').value = "IMEI"

        form.querySelector('input[name*="tipo_nro_identificador"]').classList.add('d-none')
        form.querySelector('input[name*="tipo_nro_identificador2"]').classList.add('d-none')
        form.querySelector('label[for*="tipo_nro_identificador"]').classList.add('d-none')
        form.querySelector('label[for*="tipo_nro_identificador2"]').classList.add('d-none')

        form.querySelector('input[name*="apreensao1-qtd"]').placeholder = ""
    } else if(tipo_apreensao == 'arma'){
        form.querySelector('label[for*="tipo_objeto"]').textContent = "Calibre"
        form.querySelector('input[name*="tipo_objeto"]').placeholder = "Samsung, Iphone, Motorola"

        form.querySelector('label[for*="especie_modelo"]').textContent = "Modelo"
        form.querySelector('input[name*="especie_modelo"]').placeholder = "A54, 14, G54"

        form.querySelector('select[name*="und_medida"]').value = 'UND'

        form.querySelector('label[for*="nro_identificador"]').textContent = "Nº IMEI¹"
        form.querySelector('input[name*="nro_identificador"]').placeholder = "000000-00-000000-0"
        form.querySelector('label[for*="nro_identificador2"]').textContent = "Nº IMEI²"
        form.querySelector('input[name*="nro_identificador2"]').placeholder = "000000-00-000000-0"

        form.querySelector('input[name*="tipo_nro_identificador"]').value = "IMEI"
        form.querySelector('input[name*="tipo_nro_identificador2"]').value = "IMEI"
        form.querySelector('input[name*="tipo_nro_identificador"]').classList.add('d-none')
        form.querySelector('input[name*="tipo_nro_identificador2"]').classList.add('d-none')
        form.querySelector('label[for*="tipo_nro_identificador"]').classList.add('d-none')
        form.querySelector('label[for*="tipo_nro_identificador2"]').classList.add('d-none')

        form.querySelector('input[name*="apreensao1-qtd"]').placeholder = ""
    }

    atualizarContagem()
    toggleCampos()
    mostrarInputs(form)
}

function adicionar_pessoa(target){
    var pessoas = Array.from(document.getElementById('accordionCamposEnvolvidos').querySelectorAll('.accordion-item'))
    var form = null
    var tipo_envolvio = document.getElementById('tipoEnvolvido').textContent
    var checkForm = true
    
    pessoas.every(item =>{
        form = item
        checkForm = verificarVazio(item)
        if(checkForm){
            return false;
        }else{
            return true;
        }
    })

    if(checkForm==false){ form = duplicar(form)}

    form.querySelector('.accordion-button').textContent = tipo_envolvio

    var info = target.parentElement.previousElementSibling.querySelectorAll('span')
    info.forEach(function(item) {
        var nome_campo = item.getAttribute('target')
        var campo = form.querySelector(`*[name*='${nome_campo}']`)
        if(nome_campo.includes('data') && item.textContent){
            var dateParts = item.textContent.trim().split('/')
            var formattedDate = `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`;
            campo.value = formattedDate
        }else if(nome_campo == 'pj'){
            item.textContent.trim() == 'True' ? campo.checked = true : campo.checked = false
            campo.value = 'True'
        }else{
            campo.value = item.textContent.trim()
        }
        campo.classList.remove('warning-form')
        form.querySelector(`*[name*='atuacao']`).value = tipo_envolvio.trim().toUpperCase()
    });

    atualizarContagem()
    mostrarInputs(form)
}

function duplicar(form){
    var str = form.querySelector('input').getAttribute('name').split('-')[0]
    var count = parseInt(str[str.length - 1])
    var formClone = form.cloneNode(true);
    formClone.querySelectorAll('input, select, label, div, button').forEach(function(field) {
        if(field.type == 'checkbox'){
            field.checked = false
        }else{
            field.value = ''
        }
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

function cadastrar_pessoa(tipo){
    var pessoas = Array.from(document.getElementById('accordionCamposEnvolvidos').querySelectorAll('.accordion-item'))
    var form = null
    var checkForm = true
    
    pessoas.every(item =>{
        form = item
        checkForm = verificarVazio(item)
        if(checkForm){
            return false;
        }else{
            return true;
        }
    })

    if(checkForm==false){ form = duplicar(form)}

    form.querySelector('.accordion-button').textContent = tipo
    form.querySelector(`*[name*='atuacao']`).value = tipo.trim().toUpperCase()

    atualizarContagem()
    mostrarInputs(form)    
}

function mostrarInputs(element){
    var btnItem = element.querySelector('h2').querySelector('button')
    btnItem.click()
    element.closest('.collapse').classList.add('show')
    modal_pesquisa.style.display = 'none'
    scrollToElement(element)
}

function scrollToElement(element) {
    if (element) element.scrollIntoView({ behavior: 'smooth' });
}


function removeItem(btn){
    var item = btn.closest('.accordion-item')
    var qtd_form = item.parentElement.querySelectorAll('.accordion-item').length
    if(qtd_form > 1){
        item.parentElement.removeChild(item);
    }else{
        item.closest('.collapse').classList.remove('show')
        item.querySelectorAll('input, select').forEach(function(x){
            if(x.type == 'checkbox'){
                x.checked = false
            }else{
                x.value=''
            }
        })
    }

}

function mostrarCumprimento(checkbox){
    checkbox.addEventListener("change", function () {
        camposCumprimentoMedidas.style.display = checkbox.checked ? "block" : "none";
    });
}

function mostrarApreensao(checkbox){
    checkbox.addEventListener("change", function () {

        if(checkbox.checked){
            camposApreensao.style.display = "block"
            camposApreensao.querySelectorAll('input, select').forEach(function(item){
                if(!item.classList.contains('campos-form')){
                    item.required=true
                }
            })
        }else{
            camposApreensao.style.display = "none"
            camposApreensao.querySelectorAll('input, select').forEach(function(item){
                if(!item.classList.contains('campos-form')){
                    item.required=false
                }
            })
            
        }
        requiredMark()
    });
}

// Função para mostrar ou esconder campos com base na seleção do objeto apreendido
function toggleCampos() {
    var select_objeto = document.querySelectorAll('.obj-apreendido')
    select_objeto.forEach(function(select){
        var objetoSelecionado = select.options[select.selectedIndex].value
        var campos_padrao = ["","DROGA", "MUNICAO", "RECURSO_NATURAL"];
        // Esconder todos os campos e labels relacionados a campos-form
        select.parentElement.querySelectorAll('.campos-form').forEach(function(item){
            item.style.display = 'none'; 
            item.previousElementSibling.style.display = 'none'
        })
    
        // Mostrar campos adicionais se não for uma droga, munição ou recurso natural
        if (campos_padrao.indexOf(objetoSelecionado) === -1) {
            select.parentElement.querySelectorAll('.campos-form').forEach(function(item){
                item.style.display = 'block'; 
                item.previousElementSibling.style.display = 'block'})
        }

    })

}

function togglePJ(){
    var checkbox = document.querySelectorAll('input[name*="pj"]')
    checkbox.forEach(function(item){
        if(item.checked){
            
        }
    })
}

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

$(document).ready(function() {
    $('option[value="PJ"]').hide();
    var $pj = $('input*[name*="pj"]');
    var $label = $('label*[for*="check_pj"]');
    $pj.add($label).wrapAll('<div class="form-check form-switch"></div>');
});