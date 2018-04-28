$(function(){
    $('input[name="ssx"]').cityPicker({
        title: "住宅所在省市县（区）"
    });

    $('#form5').form();

    $('#submit5').on('click', function(){
        validate_res = false;
        $('#form5').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;

        data = $('#form5').serializeForm();
        $.post('', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = './other_info';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
