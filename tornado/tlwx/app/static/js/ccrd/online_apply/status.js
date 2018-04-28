$(function(){
    $('select[name="id_type"]').val('I');
    $('#form1').form();

    $('#submit1').on('click', function(){
        validate_res = false;
        $('#form1').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;

        data = $('#form1').serializeForm();
        $.post('', data, function(resp){
            console.log(resp);
            if(resp.success){
                localStorage.setItem('ccrd_online_apply_status', JSON.stringify(resp.items));
                window.location.href = './list';
            }else{
                $.toptips(resp.msg);
            }
        })
    });

    $('.ys_vcode_img').on('click', function(){
        $.get(BASE_URL + '/common/refresh_pic_vcode', function(resp){
            $('.ys_vcode_img').attr('src', resp.url + '?v=' + Math.random());
        }).error(function(){
            $.toptips('刷新图片失败');
        });
    }).trigger('click');
});
