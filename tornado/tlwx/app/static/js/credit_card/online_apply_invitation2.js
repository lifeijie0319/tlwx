$(function(){
    query_str = decodeURI(window.location.search);
    console.log(query_str);
    invitor_name = getUrlArgs('name', query=query_str);
    $('.card_title > span[name="name"]').text(invitor_name);
    invitor_employee_id = getUrlArgs('employee_id', query=query_str);
    $('.card_title > span[name="employee_id"]').text(invitor_employee_id);
    qrcode_url = BASE_URL + '/credit_card/online_apply/page/0';
    $('#qrcode').empty().qrcode({
        width: $('#signed_qrcode').width(),
        height: $('#signed_qrcode').width(),
        text: qrcode_url,
    });
    qrcode_img = $('#qrcode > canvas')[0].toDataURL('image/png');
    $('#qrcode').html('<img style="width:100%;height:100%" src="' + qrcode_img + '">');
})
