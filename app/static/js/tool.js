var BASE_URL = 'https://hz.wx.yinsho.com/tlwx';
var APPID = 'wx6290daffb81416ac';

function getCookie(name) {
    var c = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return c ? c[1] : undefined;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
var csrftoken = getCookie('_xsrf');
console.log(csrftoken);
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-XSRFToken", csrftoken);
        }
    }
})

function getClientType(){
    var u = navigator.userAgent;
    if(u.indexOf('Android') > -1 || u.indexOf('Linux') > -1){
        return 'android';
    }else if(!!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/)){
        return 'ios';
    }else{
        return 'others';
    }
}

function rd(n,m){
    var c = m-n+1;  
    return Math.floor(Math.random() * c + n);
}

function getUrlArgs(name, query=window.location.search) { 
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i"); 
    var r = query.substr(1).match(reg); 
    if (r != null) return unescape(r[2]); return null; 
}

function configJssdk(apilist){
    $.post(BASE_URL + '/wx/jssdk', {url: window.location.href}, function(resp){
        if(resp.success){
            resp = resp.config;
            wx.config({
                debug : false,
                appId : APPID,
                timestamp : resp.timestamp,
                nonceStr : resp.nonceStr,
                signature : resp.signature,
                jsApiList : apilist,
            });
        }else{
            console.log(resp.msg);
        }
    }).error(function(xhr, textStatus, errorThrown){
        alert(xhr.status);
        alert(xhr.readyState);
        alert(textStatus);
    });
}

function wxUploadImg(img_dom, source_type=['album']){
    wx.chooseImage({
        count: 1, // 默认9
        sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
        sourceType: source_type, // 可以指定来源是相册还是相机，默认二者都有
        success: function (res) {
            var localIds = res.localIds // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片
            if(getClientType() == 'ios'){
                //alert('ios');
                wx.getLocalImgData({
                    localId: localIds[0],
                    success: function(res){
                        img_dom.attr('src', res.localData);
                        //alert(res.localData);
                    },
                    fail: function(){
                        alert('该图片暂时无法预览');
                    }
                });
            }else{
                img_dom.attr('src', localIds[0]);
            }
            wx.uploadImage({
                localId: localIds[0], // 需要上传的图片的本地ID，由chooseImage接口获得
                isShowProgressTips: 1, // 默认为1，显示进度提示
                success: function(res){
                    var serverId = res.serverId; // 返回图片的服务器端ID
                    img_dom.attr('mediaid', serverId);
                }
            });
        }
    });
}

(function($) {
    $.fn.serializeForm = function(){
        var o = {};
        var a = this.serializeArray();
        //console.log(a);
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return JSON.stringify(o);
    }

    $.fn.sendVcode = function(cellphone) {
        send_btn = $(this);
        //alert('enter send_vcode');
        //alert('disabled:', send_btn.prop('disabled'));
        //console.log(send_btn, send_btn.prop('disabled'));
        if(send_btn.prop('disabled')) return false;
        validate_res = false;
        cellphone.validate(function(error){
            if(!error) validate_res = true;
        });
        if (!validate_res) return false;
        data = {
            cellphone: cellphone.val(),
            now: new Date().getTime(),
        }
        $.post(BASE_URL + '/common/send_vcode', data, function (resp) {
            console.log(new Date().toGMTString());
            $.toptips("验证码已发送，请查收！", 'success');
        }).error(function(){
            $.toptips('服务器错误');
        });
        var times = 60;
        send_btn.prop('disabled', true);
        //console.log(send_btn, send_btn.prop('disabled'));
        timer = setInterval(function () {
            times--;
            send_btn.text(times + "秒后重试");
            if (times <= 0) {
                send_btn.text("发送验证码");
                send_btn.prop('disabled', false);
                //console.log(send_btn.prop('disabled'));
                clearInterval(timer);
                times = 60;
            }
        }, 1000);
    }
})(jQuery);
