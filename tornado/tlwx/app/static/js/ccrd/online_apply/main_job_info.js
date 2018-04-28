$(function(){
    $('input[name="ssx"]').cityPicker({
        title: "单位所在省市县（区）"
    });

    $('#form4').form();

    $('#submit4').on('click', function(){
        validate_res = false;
        $('#form4').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;

        data = $('#form4').serializeForm();
        $.post('', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = './house_info';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
