const endpoint = '/API/pesquisa/'
const resultado_div = $('.resultados_pesquisa')
let ajax_call = function (endpoint, request_parameters, input) {
    var search_icon = input.previousElementSibling.querySelector('.search-icon');
    
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            // fade out the resultado_div, then:
            resultado_div.fadeTo('fast', 0, 'linear').promise().then(() => {
                // replace the HTML contents
                resultado_div.html(response['html_from_view'])
                // fade-in the div with new contents
                resultado_div.fadeTo('fast', 1, 'linear')
                // stop animating search icon
                $(search_icon).addClass('bi-search')
                $(search_icon).removeClass('spinner-border spinner-border-sm')
            })
        })
}

var user_input = document.querySelectorAll('.input_ajax')
const delay_by_in_ms = 1000
let scheduled_function = false

user_input.forEach(function(input){
    input.addEventListener('keyup', function () {
        query(input, $(this).val())
    })
})


function query(input, valor){
    const input_value = valor;
    const chave = input.id

    var search_icon = input.previousElementSibling.querySelector('.search-icon');
    var request_parameters = {};

	if (input_value.length > 3) {
        request_parameters[chave] = input_value;

        $(search_icon).removeClass('bi-search')
        $(search_icon).addClass('spinner-border spinner-border-sm')

        // if scheduled_function is NOT false, cancel the execution of the function
        if (scheduled_function) {
            clearTimeout(scheduled_function)
        }

        // setTimeout returns the ID of the function to be executed
        scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters, input)
    }
}