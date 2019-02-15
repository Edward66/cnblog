// 头像预览功能
$('#id_avatar').change(function () {   // 图片发生了变化，所以要用change事件
                                       // 获取用户选中的文件对象
    let file_obj = $(this)[0].files[0];

    // 获取文件对象的路径
    let reader = new FileReader();  // 等同于在python里拿到了实例对象
    reader.readAsDataURL(file_obj);

    reader.onload = function () {
        // 修改img的src属性，src = 文件对象的路径
        $("#avatar_img").attr('src', reader.result);  // 这个是异步，速度比reader读取路径要快，
                                                      // 所以要等reader加载完后在执行。
    };
});

// 基于Ajax提交数据
let handlerPopup = function (captchaObj) {
    // 成功的回调
    captchaObj.onSuccess(function () {
        let validate = captchaObj.getValidate();
        let formdata = new FormData();  // 相当于python里实例化一个对象
        let request_data = $('#fm').serializeArray();
        $.each(request_data, function (index, data) {
            formdata.append(data.name, data.value)
        });
        formdata.append('avatar', $('#id_avatar')[0].files[0]);

        $.ajax({
            url: '',
            type: 'post',
            contentType: false,
            processData: false,
            data: formdata,
            success: function (data) {
                if (data.user) {
                    // 注册成功
                    location.href = '/login/'
                } else {
                    // 注册失败

                    // 清空错误信息，每次展示错误信息前，先把之前的清空了。
                    $('span.error-info').html("");
                    $('.form-group').removeClass('has-error');
                    // 展示此次提交的错误信息
                    $.each(data.msg, function (field, error_list) {
                        if (field === '__all__') {  // 全局错误信息，在全局钩子里自己定义的
                            $('#id_re_pwd').next().html(error_list[0]);
                        }
                        $('#id_' + field).next().html(error_list[0]);
                        $('#id_' + field).parent().addClass('has-error');  // has-error是bootstrap提供的
                    });
                }
            }
        })

    });
    $("#popup-submit").click(function () {
        captchaObj.show();
    });
    // 将验证码加到id为captcha的元素里
    captchaObj.appendTo("#popup-captcha");
    // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
};
// 验证开始需要向网站主后台获取id，challenge，success（是否启用failback）
$.ajax({
    url: "/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
    type: "get",
    dataType: "json",
    success: function (data) {
        // 使用initGeetest接口
        // 参数1：配置参数
        // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
        initGeetest({
            gt: data.gt,
            challenge: data.challenge,
            product: "popup", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
            offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
            // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
        }, handlerPopup);
    }
});