//获取localstorage对象
var storage = window.localStorage;
var setHour;
var setMinute;
var setSecond;

//获取用户设定时间
function getTimeSet()
{
	var winWide = window.screen.width;
	if(winWide<768)
	{
		setHour=document.getElementById("inputs1").value;
		setMinute=document.getElementById("inputs2").value;
		setSecond=document.getElementById("inputs3").value;
	}
	else
	{
		setHour=document.getElementById("input1").value;
		setMinute=document.getElementById("input2").value;
		setSecond=document.getElementById("input3").value;
	}
}

//设置模态框内容
function setText()
{
	getTimeSet();
	var winWide = window.screen.width;
	if(winWide<768)
	{
		var defiedTime=setHour*60*60*1000+setMinute*60*1000+setSecond*1000;
		storage.setItem("defiedTime",defiedTime);
	}
	else
	{
		var defiedTime=setHour*60*60*1000+setMinute*60*1000+setSecond*1000;
		storage.setItem("defiedTime",defiedTime);
	}
	document.getElementById('myModalBody').innerHTML='房间将于您离开后'+setHour+'小时'+setMinute+'分'+setSecond+'秒断电！';
}

$('#myModal').on('show.bs.modal', function () {
	document.getElementsByTagName('body')[0].style.paddingTop='0';
	document.getElementById('navbarContainer').style.position='static';
	document.getElementById('navbarContainer').style.padding='0';
	document.getElementById('container').style.zIndex='0';
})
$('#myModal').on('hidden.bs.modal', function () {
	document.getElementsByTagName('body')[0].style.paddingTop='60px';
  document.getElementById('navbarContainer').style.position='fixed';
})
function rotate()
{
	console.log(Math.random());
}
//setInterval('rotate()',1000);
//每隔2s获取一次当前房间是否有人的状态
//长轮询参数
var getting =
{
	url:'!!!',//后边再改!!!
	dataType:'json',
	success:function(res)
	{
		console.log(res);
		endCounter();
	},
	error:function(res)
	{
		$.ajax(getting);
	}
}

//点击模态框确定或标签页打开触发事件
function loadResult()
{
	var defiedTime = storage.getItem("defiedTime");//获取用户设定时间
	var xmlHttp;
	var result;//房内是否有人以及上一次房内无人的时间
	var lastLeave;
	if(window.XMLHttpRequest)
	{
		xmlHttp=new XMLHttpRequest();
	}
	else
	{
		xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlHttp.onreadystatechange=function()
	{
		if(xmlHttp.readyState==4 && xmlHttyp.status==200)
		{
			result = xmlHttp.responseText;
			lastLeave = xmlHtto.responseText; //后边根据后端数据格式再改！！！
		}
	}
	xmlHttp.open("GET","...",true);
	xmlHttp.send();
	if(result==0)
	{
		var dateNow = Date.now();
		var initTime = defiedTime - (dateNow - lastLeave);//初始化计时器的时间
		initCounter();
		//长轮询，获取到有人信号则停止计时
		$.ajax(getting);
	}
}

//监控标签页的打开和隐藏
document.addEventListener('webkitvisibilitychange',function()
			 {
					 if(document.webkitVisibilityState=='hidden')
					 {}
					 else
					 {
							 loadResult();
					 }
			 })
document.addEventListener('mozvisibilitychange',function()
			 {
					 if(document.mozVisibilityState=='hidden')
					 {
					 }
					 else
					 {
							 loadResult();
					 }
			 })

//初始化计时器并保存其初始状态
var node = null;
function initCounter()
{
	document.getElementById("container").style.margin=0;
	document.getElementById("form").style.display="none";
	document.getElementById("forms").style.display="none";
	document.getElementById("timeCounter").style.display="block";
	$(function startTime(){

		var note = $('#note'),
			ts = new Date(2012, 0, 1),
			newYear = true;
			getTimeSet();
		if((new Date()) > ts){
			ts = (new Date()).getTime() + setHour*60*60*1000+setMinute*60*1000+setSecond*1000-1;
			newYear = false;
		}

		$('#countdown').countdown({
			timestamp	: ts,
			callback	: function(hours, minutes, seconds){

				var message = "房间将于";

				message += hours + " 小时";
				message += minutes + " 分";
				message += seconds + " 秒";

				if(newYear){
					message += "left until the new year!";
				}
				else {
					message += "后断电!";
				}
				note.html(message);
			}
		});
	});
	var counterTest = document.getElementById("timeCounter");
	node = counterTest.cloneNode(true);
	return false;
}

//返回输入页面并恢复计时器初始状态
function endCounter()
{
	var oldNode = document.getElementById("timeCounter");
  oldNode.parentNode.replaceChild(node, oldNode);
	var winWide = window.screen.width;
	if(winWide<768)
	{
		document.getElementById("forms").style.display="block";
	}
	else
	{
		document.getElementById("form").style.display="block";
	}
	document.getElementById("timeCounter").style.display="none";
	return false;
}
