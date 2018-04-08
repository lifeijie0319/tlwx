//toptips
+ function($) {
    "use strict";
    var timeout;
    $.toptips = function(text, duration, type) {
        if (!text) return;
        if (typeof duration === typeof "a") {
            type = duration;
            duration = undefined;
        }
        var duration = duration || 2000;
        var className = type ? 'bgcolor_' + type : 'bgcolor_danger';
        var $t = $('.ys_toptips').remove();
        $t = $('<div class="ys_toptips"></div>').appendTo(document.body);
        $t.html(text);
        $t[0].className = 'ys_toptips ' + className
        clearTimeout(timeout);
        if (!$t.hasClass('ys_toptips_visible')) {
            $t.show().width();
            $t.addClass('ys_toptips_visible');
        }
        timeout = setTimeout(function() {
            $t.removeClass('ys_toptips_visible');
                setTimeout(function() {
                    $t.remove();
                }, 300);
        }, duration);
    }
}($);
//from validate
(function() {
    $.cell_validate = _validate;//added by lifeijie
    function _validate($input) {
        var input = $input[0],
            val = $input.val();
        //added by lifeijie
        if (!input.getAttribute("emptyTips") && !$input.val().length) {
            return null;
        }
        //added by lifeijie
        if (input.tagName == "INPUT" || input.tagName == "TEXTAREA") {
            var reg = input.getAttribute("required") || input.getAttribute("pattern") || "";
            if (!$input.val().length) {
                return "empty";
            } else if (reg) {
                return new RegExp(reg).test(val) ? null : "notMatch";
            } else {
                return null;
            }
        } else if (input.getAttribute("type") == "checkbox" || input.getAttribute("type") == "radio") {
            return input.checked ? null : "empty";
        } else if (val.length) {
            return null;
        }
        return "empty";
    }

    function _showErrorMsg(error) {
        if (error) {
            var $dom = error.$dom,
                msg = error.msg,
                tips = $dom.attr(msg + "Tips") || $dom.attr("tips") || $dom.attr("placeholder");
            if (tips) $.toptips(tips);
            $dom.parents(".ys_cell").addClass("color_danger");
        }
    }
    var oldFnForm = $.fn.form;
    $.fn.form = function() {
        return this.each(function(index, ele) {
            var $form = $(ele);
            $form.find("[required]").on("blur", function() {
                var $this = $(this),
                    errorMsg;
                if ($this.val().length < 1) return;
                errorMsg = _validate($this);
                if (errorMsg) {
                    _showErrorMsg({
                        $dom: $this,
                        msg: errorMsg
                    });
                }
            }).on("focus", function() {
                var $this = $(this);
                $this.parents(".ys_cell").removeClass("color_danger");
            });
        });
    };
    $.fn.form.noConflict = function() {
        return oldFnForm;
    };
    var oldFnValidate = $.fn.validate;
    $.fn.validate = function(callback) {
        return this.each(function() {
            var $requireds = $(this).find("[required]");
            if (typeof callback != "function") callback = _showErrorMsg;
            for (var i = 0, len = $requireds.length; i < len; ++i) {
                var $dom = $requireds.eq(i),
                    errorMsg = _validate($dom),
                    error = {
                        $dom: $dom,
                        msg: errorMsg
                    };
                if (errorMsg) {
                    if (!callback(error)) _showErrorMsg(error);
                    return;
                }
            }
            callback(null);
        });
    };
    $.fn.validate.noConflict = function() {
        return oldFnValidate;
    };
})();
