$(function(){
    from = getUrlArgs('from');
    switch(from){
        case 'bind':
            $('#content').html('绑定信用卡成功');
            break;
        case 'binded':
            $('#content_title').html('提示');
            $('#content').html('您已经绑定信用卡，请不要重复提交');
            break;
        case 'unbind':
            $('#content').html('解绑信用卡成功');
            break;
        case 'unbinded':
            $('#content_title').html('提示');
            $('#content').html('您已经解绑信用卡，请不要重复提交');
            break;
        case 'activate':
            $('#content_title').html('激活成功');
            $('#content').html('您已经成功激活信用卡');
            break;
        case 'ccrd_online_apply':
            $('#content').html('您的信用卡申请已提交，请等待银行审核');
            break;
        case 'installment_bill':
            $('#content').html('您的账单分期申请已成功');
            break;
        case 'installment_cash':
            $('#content').html('您的现金分期申请已成功');
            break;
        case 'installment_lg_cash':
            $('#content').html('您的大额现金分期申请已成功');
            break;
        case 'installment_consumption':
            $('#content').html('消费分期申请成功');
            break;
        case 'error':
            $('.ys_prompt_icon > i').removeClass('icon-correct_big').addClass('icon-close-fill color_danger');
            $('#content_title').html('页面加载失败');
            url = decodeURI(window.location.search);
            console.log(url);
            msg = getUrlArgs('error_msg', url);
            $('#content').html(msg);
            break;
        default:
    }
});
