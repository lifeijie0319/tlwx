$(function(){
    $('#form1').form();

    $('#submit1').on('click', function(){
        validate_res = false;
        $('#form1').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;
        data = $('#form1').serializeForm();
        localStorage.setItem('ccrd_online_apply_data', data);
        window.location.href = '2';
    });

    $('#send_vcode').on('click', function () {
         sendVcode($(this), $('input[name="cel"]'));
    });

    /*$('.ys_vcode_img').on('click', function(){
        $.get(BASE_URL + '/common/refresh_pic_vcode', function(resp){
            $('.ys_vcode_img').attr('src', resp.url + '?v=' + Math.random());
        }).error(function(){
            $.toptips('刷新图片失败');
        });
    }).trigger('click');*/
});
