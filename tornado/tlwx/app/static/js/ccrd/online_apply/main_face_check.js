$(function(){
    configJssdk(['chooseImage','uploadImage']);

    $('.id_card_wrapper').on('click', function(){
        img_dom = $(this).find('img');
        if(img_dom.attr('mediaid') || img_dom.attr('mediaid')){
            $.confirm('您最多只能上传1张图片，是否删除原来的图片重新选择？', function(){
                wxUploadImg(img_dom, source_type=['camera']);
            },function(){
            });
        }else{
            wxUploadImg(img_dom, source_type=['camera']);
        }
    });

    $('#submit7').on('click', function(){
        face = $('#face').attr('mediaid');
        if(!face){
            $.alert('请拍摄您的人脸照片');
            return false;
        }
        params = JSON.stringify({
            imgs: [
                {
                    mediaid: face,
                    dirname: 'face',
                }
            ]
        });
        console.log(params);
        $.post(BASE_URL + '/wx/upload_img', params, function(resp){
            if(resp.success){
                $.toptips('图片存储成功', 'success');
                window.location.href = BASE_URL + '/staticfile/done.html?from=ccrd_online_apply';
            }else{
                $.toptips('图片存储失败');
            }
        }).error(function(){
            $.toptips('服务器错误');
        });
    });
});
