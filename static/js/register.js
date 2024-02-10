
function bindEmailCaptchaChick(){
      $('#captcha-btn').click(function (event){
         var $but = $(this)
        event.preventDefault();
        var email = $('input[name="email"]').val();
        $.ajax({
            url: '/auth/captcha/email?email='+email,
            method:'GET',
            success:function (result){
                if (result['code'] == 200){
                    console.log(result['data'])
                    var countdown = 5;
                    $but.off('click');
                    var timer = setInterval(function (){
                        $but.text(countdown);
                        console.log(countdown);
                        countdown -= 1;
                        if (countdown <= 0){
                            $but.text('获取验证码')
                            clearInterval(timer)
                            bindEmailCaptchaChick();
                        }
                    }, 1000);
                    alert('邮箱验证码发送成功');
                }else{
                    alert(result['message']);
                }
            },
            fail: function (error){
                console.log(error);
            }
        })
    //     ajax


    })
}

$(function (){
    bindEmailCaptchaChick();

})


