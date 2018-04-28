$(function(){
    $('a[name="continue"]').on('click', function(){
        setCookie('product_cd', $(this).attr('product_cd'));
    });
});
