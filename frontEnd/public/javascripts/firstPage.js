//获取sessionStorage
var localStorage = window.sessionStorage;

window.onclick = function(){
  var now = new Date();
  localStorage.setItem("lastClick",now.getTime());
}
function hidePNotice()
{
  document.getElementById('passwordNotice').innerHTML='';
}

function hideNNotice()
{
  document.getElementById('numberNotice').innerHTML='';
}

$(document).ready(function()
{
    $('#defaultForm')
      .bootstrapValidator(
        {
            message: 'This value is not valid',
            feedbackIcons:
            {
                valid: 'glyphicon glyphicon-ok',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields:
            {
                roomNumber:
                {
                },
                thePassword:
                {
                }
            }
        })
      .on('error.validator.bv', function(e, data)
      {
            data.element
                .data('bv.messages')
                // 隐藏所有提示信息
                .find('.help-block[data-bv-for="' + data.field + '"]').hide()
                // 只显示当前一条相关提示信息
                .filter('[data-bv-validator="' + data.validator + '"]').show();
        })
        .on('success.form.bv',function (e)
        {
          e.preventDefault();//避免重复提交
          var $form = $(e.target);
          var bootstrapValidator = $form.data('bootstrapValidator');
          $.ajax({
            type: 'POST',
            url:'http://localhost:8000/login/login',
            dataType: 'json',
            data: {"roomNumber": document.getElementById('roomNumber').value,
                   "thePassword": document.getElementById('thePassword').value},
            // 下面两个参数解决跨域问题
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            complete: function(XMLHttpRequest, textStatus) {},
            success: function(data) {
              document.getElementById('numberNotice').innerHTML='';
              document.getElementById('passwordNotice').innerHTML='';
              if(document.getElementById('roomNumber').value == '')
              {
                bootstrapValidator.updateStatus('roomNumber', 'INVALID','');
                document.getElementById('numberNotice').innerHTML="请输入账号";
              }
              if(document.getElementById('thePassword').value == '')
              {
                bootstrapValidator.updateStatus('thePassword', 'INVALID','');
                document.getElementById('passwordNotice').innerHTML="请输入密码";
              }
              if(document.getElementById('thePassword').value != ''&&document.getElementById('roomNumber').value != '')
              {
                var now = new Date();
                if(data.login_result == 1)
                {
                  window.location.href = '/userPage';
                  localStorage.setItem("user","commonUser");
                  localStorage.setItem("loginTime",now.getTime())
                }
                else if(data.login_result == 0)
                {
                  window.location.href = '/admin';
                  localStorage.setItem("user","admin");
                  localStorage.setItem("loginTime",now.getTime())
                }
                else if(data.login_result == 2)
                {
                  //bootstrapValidator.updateStatus('thePassword', 'INVALID','');
                  document.getElementById('passwordNotice').innerHTML="用户名和密码不匹配";
                  //bootstrapValidator.updateMessage('thePassword','notEmpty','密码错误');
                  console.log("passwordincorrect");
                }
              }
            },
            error: function(err) {
                console.log(err);
            }
          });
        });
});
