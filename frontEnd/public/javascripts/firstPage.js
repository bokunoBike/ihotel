function login()
{
  var roomNumber=document.getElementById('roomNumber');
  var password=document.getElementById('password');
  var xmlhttp;
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
                    message: 'The username is not valid',
                    validators:
                    {
                        notEmpty:
                        {/*非空提示*/
                            message: '房号不能为空'
                        },
                        regexp:
                        {/* 正则表达式*/
                           regexp: /^[0-9]*[1-9][0-9]*$/,
                           message: '请检查房号正确性'
                       },
                        stringLength:
                        {/*长度提示*/
                            min: 3,
                            max: 4,
                            message: '请检查房号正确性'
                        },
                        threshold: 3,
                        remote:
                        {
                          url:'后边改！！！',
                          message: '房号不存在',
                          delay: 1000,
                          type:'POST',
                          data: {"roomNumber": document.getElementById('roomNumber').value}
                        }
                    }
                },
                thePassword:
                {
                    //trigger: 'blur',
                    message:'密码无效',
                    validators:
                    {
                        notEmpty:
                        {
                            message: '密码不能为空'
                        },
                        threshold: 6,
                        regexp:
                        {/* 正则表达式*/
                           regexp: /(^\d{5}(\d|X|x)$)/,
                           message: '密码错误'
                       },
                        stringLength:
                        {
                            min: 6,
                            max: 6,
                            message: '密码错误'
                        }
                    }
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
          var bv = $form.data('bootstrapValidator');
          $.post($form.attr('action'),$form.serialize(),function(result){
            if(result.valid==true)
            {
              window.location.href='http://localhost:3000/userPage';
            }
            else
            {
              bootstrapValidator.updateStatus('thePassword', 'INVALID').validateField('username');
              //$('#defaultForm').data(“bootstrapValidator”).updateStatus("thePassword",  "NOT_VALIDATED",  null );
              bootstrapValidator.updateMessage('thePassword',null,'密码错误');
            }
          },'json');
        });
});
