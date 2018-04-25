$(function(){
    $('#face').on('change', function(){
        img = getObjectURL(this.files[0]);
        $('#preview').attr('src', img);
    });
    $('#upload').on('click', function(){
        formdata = new FormData();
        img = $('#face')[0].files[0];
        console.log(img);
        formdata.append('photo', img);
        formdata.append('dirname', 'face');
        $.toptips('正在上传', 'success');
        $.ajax({
            url: BASE_URL + '/common/upload_img',
            type: 'post',
            contentType: false,
            processData: false,
            data: formdata,
            success: function(resp){
                if(resp.success){
                    $.toptips('上传成功', 'success');
                }else{
                    $.toptips('上传失败');
                }
            },
            error: function(){
                $.toptips('服务器错误');
            }
        });
    });
    $('#detect').on('click', function(){
        api_url = 'https://yun.anytec.cn';
        formdata = new FormData();
        img = $('#face')[0].files[0];
        console.log(BASE_URL);
        formdata.append('photo1', img);
        //formdata.append('photo2', BASE_URL + '/media/face/oSDTiwjobsmlFZNmNsvqvZsBLXLk.jpg');
        formdata.append('photo2', BASE_URL + '/media/front_id/oSDTiwq1vFtLARyBeBGhRpNeXczA.jpg');
        $.ajax({
            url: api_url + '/n-tech/v0/verify',
            type: 'post',
            contentType: false,
            processData: false,
            data: formdata,
            success: function(resp){
                console.log(resp);
            },
            error: function(){
                console.log('error');
            }
        }); 
    });
});
