$(function(){
    $('#form3').form();

    configJssdk(['chooseImage','uploadImage']);
    $('a[name="upload_img_btn"]').on('click', function(){
        img_dom = $(this).parents('.ys_cell').find('img');
        wxUploadImg(img_dom);
        img_dom.parent().attr('href', img_dom.attr('src'));
    });

    //生成协议文本
    $.get(BASE_URL + '/static/doc/ccrd/1.txt', function(resp){
        $('#protocol1').html('<pre>' + resp + '</pre>');
    });
    $.get(BASE_URL + '/static/doc/ccrd/2.txt', function(resp){
        $('#protocol2').html('<pre>' + resp + '</pre>');
    });
    $('.ys_agree_clause').on('click', function(){
        $('.ys_fixed_footer').addClass('clause_btn_visible');
    });
    $('.ys_fixed_footer').on('click', function(){
        $(this).removeClass('clause_btn_visible');
    });

    $('#submit3').on('click', function(){
        validate_res = false;
        $('#form3').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;

        id_start_date = $('input[name="id_start_date"]').val();
        id_last_date = $('input[name="id_last_date"]').val();
        if(id_start_date > id_last_date){
            $.toptips('证件有效期（起始日）大于证件有效期（到期日）');
            return false;
        }
        data = $('#form3').serializeForm();
        $.post('', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = './job_info';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
