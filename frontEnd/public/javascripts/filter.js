var localStorage = window.sessionStorage;

window.onload = checkLogin();
window.onclick = function(){
  //alert("hhh");
  var now = new Date();
  //console.log(now.getTime());
  localStorage.setItem("lastClick",now.getTime());
}

function checkLogin()
{
  var user = localStorage.getItem("user");
  var url = window.location.href.split('/');
  var now = new Date();
  var lastClick = localStorage.getItem("lastClick");
  var loginTime = localStorage.getItem("loginTime");
  if(loginTime == null)
  {
    loginTime = now.getTime();
  }
  if((now.getTime() - lastClick) >= 1800000||(now.getTime() - loginTime) >= 864000000)
  {
    localStorage.removeItem("user");
    window.location.href = '/';
  }
  else
  {
    //未登录则直接返回登录界面
    if(user == null)
    {
      window.location.href = '/';
    }
    //用户url访问管理员界面则返回用户界面
    else if(url[3] == 'userPage'&&user == 'admin')
    {
      window.location.href = '/admin';
    }
    //管理员url访问用户界面则返回管理员界面
    else if(url[3] == 'admin'&&user == 'commonUser')
    {
      window.location.href = '/userPage';
    }
  }
}

function logout()
{
  localStorage.removeItem("user");
  console.log(localStorage.getItem("user"));
  $.ajax({
    type: 'POST',
    url:'http://' + host + ':8000/user/get_expire_time',
    dataType: 'json',
    // 下面两个参数解决跨域问题
    xhrFields: {
        withCredentials: true
    },
    crossDomain: true,
    complete: function(XMLHttpRequest, textStatus) {},
    success: function(data)
    {
      console.log(data);
    },
    error: function(err) {
        console.log(err);
    }
  });
}
