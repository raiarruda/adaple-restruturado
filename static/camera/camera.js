function getCookie(name) {
   
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {

        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

    }
});


var formData = new FormData();
// capture camera and/or microphone


navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(function (camera) {

    var recorder;

    document.getElementById('iniciar').onclick = (function (){
        this.disabled = true;
      
        document.getElementById('your-video-id').muted = true;
        setSrcObject(camera, document.getElementById('your-video-id'));
        recorder = RecordRTC(camera, { type: 'video'});
        recorder.startRecording();

        document.getElementById('terminar').disabled =false;
    });

   
    //iniciar a funcao de graavar video apos apertar botao terminar
    document.getElementById('terminar').onclick = (function () {
        document.getElementById('salvar-form-com-video').disabled=false;
        this.disabled = true;
        recorder.stopRecording(function () {

            // get recorded blob
            var blob = recorder.getBlob();
            // generating a random file name
            var fileName = getFileName('webm');
            console.log(fileName);
            // we need to upload "File" --- not "Blob"
            var fileObject = new File([blob], fileName, {
                type: 'video/webm'
            });

            // recorded data
            formData.append('video', fileObject);
            // file name
            formData.append('video-filename', fileObject.name);
            // document.getElementById('h').innerHTML = 'Uploading to PHP using jQuery.... file size: (' + bytesToSize(fileObject.size) + ')';
            // upload using jQuery
          
            // release camera
            // document.getElementById('your-video-id').srcObject = document.getElementById('your-video-id').src = null;
           
            camera.getTracks().forEach(function (track) {
                track.stop();
            });
        });

        
    }); //fecha a função de terminar o video

});


























// this function is used to generate random file name
function getFileName(fileExtension) {
    var d = new Date();
    var year = d.getUTCFullYear();
    var month = d.getUTCMonth();
    var date = d.getUTCDate();
    return 'RecordRTC-' + year + month + date + '-' + getRandomString() + '.' + fileExtension;
}
function getRandomString() {
    if (window.crypto && window.crypto.getRandomValues && navigator.userAgent.indexOf('Safari') === -1) {
        var a = window.crypto.getRandomValues(new Uint32Array(3)),
            token = '';
        for (var i = 0, l = a.length; i < l; i++) {
            token += a[i].toString(36);
        }
        return token;
    } else {
        return (Math.random() * new Date().getTime()).toString(36).replace(/\./g, '');
    }
}
