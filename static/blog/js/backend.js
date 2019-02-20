// 删除文章
$('#delete_article').click(function () {
    let nid = $(this).attr('nid');
    $.ajax({
        url: `/cn_backend/delete_article/${nid}/`,
        type: 'post',
        data: {
            nid: nid,
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        },
        success: function (data) {
            if (data.status) {
                location.reload();
            }
        }
    })
});