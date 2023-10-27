const imagemCapturada = document.getElementById('imagemCapturada')
const foto_abordado = document.getElementById('foto_abordado')
const input_imagem = document.getElementById('fileInput')

input_imagem.addEventListener('change', function(event) {
  var fileInput = event.target;
  var file = fileInput.files[0];
  
  if (file) {
    var reader = new FileReader();
    
    reader.onload = function(e) {
      var base64Data = e.target.result;
      document.getElementById('hiddenBase64Input').value = base64Data;
      imagemCapturada.style.display = 'block'
      imagemCapturada.src = base64Data;
      foto_abordado.value = fileInput.files[0].name
    };
    
    reader.readAsDataURL(file);
  }
});
