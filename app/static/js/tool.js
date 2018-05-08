//var BASE_URL = 'https://hz.wx.yinsho.com/tlwx';
var BASE_URL = 'http://10.252.22.131:8002/tlwx';
var APPID = 'wx6290daffb81416ac';
var PUB_KEY = '-----BEGIN PUBLIC KEY-----\
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC3K9zrxu/uT/TfEzmCv0D0RA5\
/pK53JR4VJcHbabvBzSKAR9pn1bpjfWIjmqUO/mKndJpy+ha3tzcNPdZ+uKn0+uQ\
QjQRDtsufovhZyRDWRPw9e+cS+C7GutzS4vEstudX+eScgaMPTCdBRQNpYdiK0WV\
ovVAB3BoWAEpB2yQVQIDAQAB\
-----END PUBLIC KEY-----'

function setCookie(c_name,value,expiredays)
{
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + expiredays);
    document.cookie = c_name + "=" + escape(value) + ((expiredays==null) ? "" : ";expires=" + exdate.toGMTString())
}
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
        $.showLoading();
    },
    complete: function(){
        $.hideLoading();
    },
    error: function(){
        $.toptips('服务器错误');
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

function getObjectURL(file) {  
    var url = null ;   
    // 下面函数执行的效果是一样的，只是需要针对不同的浏览器执行不同的 js 函数而已  
    if (window.createObjectURL!=undefined) { // basic  
        url = window.createObjectURL(file) ;  
    } else if (window.URL!=undefined) { // mozilla(firefox)  
        url = window.URL.createObjectURL(file) ;  
    } else if (window.webkitURL!=undefined) { // webkit or chrome  
        url = window.webkitURL.createObjectURL(file) ;  
    }  
    return url ;  
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
        if(send_btn.prop('disabled')) return false;
        if(typeof cellphone == 'string'){
            cellphone_val = cellphone;
        }else{
            console.log(cellphone, typeof cellphone == 'string');
            validate_res = false;
            cellphone.parents('.ys_cell').validate(function(error){
                if(!error) validate_res = true;
            });
            if (!validate_res) return false;
            cellphone_val = cellphone.val();
        }
        data = {
            cellphone: cellphone_val,
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
    $.fn.infoCheck = function(){
        vcode_btn = $(this);
        if(vcode_btn.prop('disabled')) return false;
        validate_res = false;
        $('form').validate(function(error){
            if (error){
                dom_name = error.$dom.attr('name');
                console.log(dom_name);
                if(dom_name != 'idno' && dom_name != 'ccrdno'){
                    return true;
                }
                return false;
            }else{
                validate_res = true;
            }
        });
        if (!validate_res) return;

        data = JSON.stringify({
            'idno': $('input[name="idno"]').val(),
            'ccrdno': $('input[name="ccrdno"]').val(),
        });
        var encrypt = new JSEncrypt();
        encrypt.setPublicKey(PUB_KEY);
        data = encrypt.encrypt(data);
        $.post(BASE_URL + '/common/info_check', data, function(resp){
            console.log(resp);
            if(resp.success){
                tips = '即将向尾号为' + resp.cellphone.slice(-4) + '的手机发送短信验证码，请确认';
                title = '短信验证码发送确认';
                $.confirm(tips, title, function(){
                    vcode_btn.sendVcode(resp.cellphone);
                },function(){
                    console.log('cancel');
                });
            }else{
                $.toptips(resp.msg);
            }
        });
    }
})(jQuery);

//toast
+ function($) {
  "use strict";

  var defaults;

  var show = function(html, className) {
    className = className || "";
    var mask = $("<div class='ys_mask_transparent'></div>").appendTo(document.body);

    var tpl = '<div class="ys_toast ' + className + '">' + html + '</div>';
    var dialog = $(tpl).appendTo(document.body);

    dialog.show();
    dialog.addClass("ys_toast_visible");
  };

  var hide = function() {
    $(".ys_mask_transparent").remove();
    $(".ys_toast_visible").remove();
  }

  $.showLoading = function(text) {
    var html = '<div class="ys_loader"></div>';
    html += '<p class="ys_toast_content">' + (text || "加载中") + '</p>';
    show(html, 'ys_toast_icontext');
  }

  $.hideLoading = function() {
    hide();
  }

}($);
