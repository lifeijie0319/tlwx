$(function(){
    $('#form3').form();

    configJssdk(['chooseImage','uploadImage']);
    $('a[name="upload_img_btn"]').on('click', function(){
        img_dom = $(this).parents('.ys_cell').find('img');
        wxUploadImg(img_dom);
        img_dom.parent().attr('href', img_dom.attr('src'));
    });

    //生成协议文本
    $.get(BASE_URL + '/static/doc/credit_card/1.txt', function(resp){
        $('#protocol1').html('<pre>' + resp + '</pre>');
    });
    $.get(BASE_URL + '/static/doc/credit_card/2.txt', function(resp){
        $('#protocol2').html('<pre>' + resp + '</pre>');
    });
    $('.ys_agree_clause').on('click', function(){
        $('.ys_fixed_footer').addClass('clause_btn_visible');
    });
    $('.ys_fixed_footer').on('click', function(){
        $(this).removeClass('clause_btn_visible');
    });

    //回显首页填入数据
    data = JSON.parse(localStorage.getItem('credit_card_online_apply_data'));
    console.log(typeof data, data);
    $('input[name="name"]').val(data.name).attr('disabled', true);
    $('input[name="idno"]').val(data.idno).attr('disabled', true);
    $('input[name="cel"]').val(data.cel).attr('disabled', true);
    /*$('#send_vcode').on('click', function () {
         sendVcode($(this), $('input[name="cel"]'));
    });*/
    $('#submit3').on('click', function(){
        validate_res = false;
        $('#form3').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;
        window.location.href = '4';
    });
});
