document.getElementById("fileInput").addEventListener("change", function (e) {// Referencie os elementos HTML
      const file = e.target.files[0];
          if (file) {
                  const reader = new FileReader();
                          reader.onload = function (e) {
                                      const base64Image = e.target.result;
                                                  // Aqui você pode enviar o `base64Image`para a sua view Django usando uma requisição AJAX.
                                                          };
                                                                  reader.readAsDataURL(file);
                                                                      }
                                                                      });
                                                                      
const abrirCamera = document.getElementById('abrirCamera');
const cameraModal = document.getElementById('cameraModal');
const cameraView = document.getElementById('cameraView');
const capturarFotoModal = document.getElementById('capturarFotoModal');
const imagemCapturada = document.getElementById('imagemCapturada');
const imagemCapturada_src = document.getElementById('imagemCapturada_src');
const imagemCapturada_input = document.getElementById('foto_abordado');
const alternarCamera = document.getElementById('alternarCamera');

let currentCamera = 'user';

// Evento para abrir o modal da câmera
abrirCamera.addEventListener('click', function () {
  navigator.mediaDevices.enumerateDevices()
    .then(function (devices) {
      const videoDevices = devices.filter(device => device.kind === 'videoinput');
      if (videoDevices.length === 0) {
        console.error('Não há câmeras disponíveis.');
        return;
      }

      let selectedDeviceId;
      if (videoDevices.length === 1) {
        selectedDeviceId = videoDevices[0].deviceId;
      } else {
        // Se houver mais de uma câmera, alterne entre elas
        selectedDeviceId = (currentCamera === 'user') ? videoDevices[0].deviceId : videoDevices[1].deviceId;
      }

      // Solicite permissão para acessar a câmera selecionada
      const constraints = {
        video: { deviceId: { exact: selectedDeviceId } }
      };

      navigator.mediaDevices.getUserMedia(constraints)
        .then(function (stream) {
          cameraModal.style.display = 'block';
          cameraView.srcObject = stream;
          // Quando o usuário clicar no botão "Capturar" no modal
          capturarFotoModal.addEventListener('click', function () {
            const canvas = document.createElement('canvas');
            canvas.width = cameraView.videoWidth;
            canvas.height = cameraView.videoHeight;
            canvas.getContext('2d').drawImage(cameraView, 0, 0, canvas.width, canvas.height);
            const dataURL = canvas.toDataURL('image/png');
            // Exiba a imagem capturada no local desejado
            imagemCapturada.src = dataURL;
            imagemCapturada.style.display = 'block'
            imagemCapturada_src.value = dataURL; 
            imagemCapturada_input.value = dataURL; 
            // Encerre o acesso à câmera e feche o modal
            stream.getTracks().forEach(function (track) {
              track.stop();
            });
            cameraModal.style.display = 'none';
          });
        })
        .catch(function (error) {
          console.error('Erro ao acessar a câmera:', error);
        });
    })
    .catch(function (error) {
      console.error('Erro ao enumerar dispositivos:', error);
    });
});

// Evento para alternar entre as câmeras
alternarCamera.addEventListener('click', function () {
  currentCamera = (currentCamera === 'user') ? 'environment' : 'user';
  abrirCamera.click(); // Recarregar o modal da câmera com a câmera selecionada
});










// imagemCapturada.style.display = 'block'
// imagemCapturada_src.value = dataURL; 
// imagemCapturada_input.value = dataURL; 