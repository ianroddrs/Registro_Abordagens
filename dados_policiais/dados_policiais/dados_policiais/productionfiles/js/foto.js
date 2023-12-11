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

input_imagem.addEventListener('change', function(event) {
  var fileInput = event.target;
  var file = fileInput.files[0];
  
  if (file) {
   var reader = new FileReader();
   
   reader.onload = function(e) {
     var img = new Image();
     img.onload = function() {
       var MAX_WIDTH = 300;
       var MAX_HEIGHT = 300;
       var width = img.width;
       var height = img.height;
 
       // Change the resizing logic
       if (width > height) {
         if (width > MAX_WIDTH) {
           height *= MAX_WIDTH / width;
           width = MAX_WIDTH;
         }
       } else {
         if (height > MAX_HEIGHT) {
           width *= MAX_HEIGHT / height;
           height = MAX_HEIGHT;
         }
       }
 
       var canvas = document.createElement("canvas");
       canvas.width = width;
       canvas.height = height;
       var ctx = canvas.getContext("2d");
       ctx.drawImage(img, 0, 0, width, height);
 
       var mimeType = "image/jpeg";
       var quality = 0.7; // Adjust the quality
       canvas.toBlob(function(blob) {
         var base64Data = URL.createObjectURL(blob);
         document.getElementById('hiddenBase64Input').value = base64Data;
         imagemCapturada.style.display = 'block'
         imagemCapturada.src = base64Data;
         foto_abordado.value = fileInput.files[0].name
       }, mimeType, quality);
     }
     img.src = e.target.result;
   };
   
   reader.readAsDataURL(file);
  }
 });
 
