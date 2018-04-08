$(function(){
    from = getUrlArgs('from');
    switch(from){
        case 'credit_card_online_apply':
            $('#content').html('您的信用卡申请已提交，请等待银行审核');
            break;
        default:
    }
});
