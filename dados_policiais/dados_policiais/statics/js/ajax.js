// const user_input = $("#input_pesquisa")
const user_input = $("#input_pesquisa")
const user_input2 = $("#input_comando")
const search_icon = $('#search-icon')
const resultado_div = $('.resultados_pesquisa')
const endpoint = '/add_pessoa/'
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
    queryPessoa('q', $(this).val())
})

user_input2.on('keyup', function () {
    queryPessoa('p', $(this).val())
})


function queryPessoa(tipo, valor){
    const input_value = valor;
    var request_parameters;
	if (input_value.length > 3) {
        if(tipo == 'q'){
            request_parameters = {q: input_value}
        }else if(tipo == 'p'){
            request_parameters = {p: input_value}
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
}