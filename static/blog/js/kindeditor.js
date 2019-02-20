KindEditor.ready(function (K) {
    window.editor = K.create('#id_content', {
        width: '800px',
        height: '500px',
        resizeType: 0,
        uploadJson: '/upload/',
        extraFileUploadParams: {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        },
        filePostName: 'upload_img',
    });
});