$(function(){
    $('form').form();
    $('select[name="num"]').on('change', function(){
        total_amount = $('input[name="total_amount"]');
        data = JSON.stringify({
            'CURR_CD': $('select[name="currency"]').val(),
            'LOAN_INIT_PRIN': total_amount.val(),
            'LOAN_INIT_TERM': $('input[name="num"]').val(),
            'LOAN_FEE_METHOD': 'E',
            'OPT': '0',
        });
        $.post(BASE_URL + '/ccrd/installment/bill', data, function(resp){
            console.log(resp);
            if(resp.success){
                $('input[name="period_pay"]').val(resp.loan_fixed_pmt_prin);
                $('input[name="total_fee"]').val(resp.loan_init_fee1);
            }else{
                $.toptips(resp.msg);
            }
        });
    });
    $('#submit').on('click', function(){
        validate_res = false;
        $('form').validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res){
            $(this).val('');
            return false;
        }
        data = JSON.stringify({
            'CURR_CD': $('select[name="currency"]').val(),
            'LOAN_INIT_PRIN': total_amount.val(),
            'LOAN_INIT_TERM': $('input[name="num"]').val(),
            'LOAN_FEE_METHOD': 'E',
            'OPT': '1',
        });
        $.post(BASE_URL + '/ccrd/installment/bill', data, function(resp){
            console.log(resp);
            if(resp.success){
                window.location.href = BASE_URL + '/staticfile/done.html?from=installment_consumption';
            }else{
                $.toptips(resp.msg);
            }
        });
    });
});
