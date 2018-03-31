myChart = echarts.init(document.getElementById('main-window'),'dark');
document.getElementById('changePersonNumber').style.display = 'block';
var systemPersonNumber;//系统检测的人数，从后端获取！！！
var changeNumber;
var nowPerson;
var clickChange = false;

window.onload = getPersonNumber();
//通过webSocket获取系统判定人数
function getPersonNumber()
{
	var host = window.location.hostname;
	var ws = new WebSocket("ws://"+host+":8000/user/get_room_info");
	window.ws = ws;
	ws.onmessage = function (e)
	{
		var data = JSON.parse(e.data);
		systemPersonNumber = data.people_counts;
		document.getElementById('number').innerHTML = systemPersonNumber;
	}
	ws.onopen = function()
	{
		console.log("wsopen");
	}
	ws.onclose = function()
	{
		ws.send(0);
	}
	ws.onerror = function(e)
	{
		ws.send(0);
	}
}
//点击增加人数
function addPerson()
{
	clickChange = true;
	window.ws.close();
	nowPerson = document.getElementById('number').innerHTML;
	changeNumber = Number(nowPerson)+1;
	document.getElementById('number').innerHTML = changeNumber;
}
//点击减少人数
function subPerson()
{
	clickChange = true;
	window.ws.close();
	nowPerson = document.getElementById('number').innerHTML;
	changeNumber = Number(nowPerson)-1;
	if(changeNumber >=0)
	{
		document.getElementById('number').innerHTML = changeNumber;
	}
}
//设置系统人数
function setPersonNumber()
{
	$.ajax({
		type: 'POST',
		url:'http://' + host + ':8000/manager/set_room_people_counts',
		dataType: 'json',
		data:{"room_id":'Z101',
			"people_counts":document.getElementById('number').value},
		// 下面两个参数解决跨域问题
		xhrFields: {
				withCredentials: true
		},
		crossDomain: true,
		complete: function(XMLHttpRequest, textStatus) {},
		success: function(data)
		{
			getPersonNumber();//人数设置成功后再开启websocket
		},
		error: function(err) {
			console.log(err);
		}
	});
}
//修改人数
function sendModify()
{
	document.getElementById('feedback').style.display = 'block';
	if((systemPersonNumber == changeNumber)||(clickChange == false))
	{
		document.getElementById('feedback').innerHTML = '您修改的人数与系统检测人数一致!';
	}
	else
	{
		document.getElementById('feedback').innerHTML = '修改成功!';
	}
	if(clickChange == true)
	{
		setPersonNumber();
	}
}
function showPersonNumber()
{
	var windowWidth=document.documentElement.clientWidth;
	if(windowWidth<768)
	{
		document.getElementById('form').style.display="block";
		document.getElementById('main-window').style.display="none";
		document.getElementById('changePersonNumber').style.visibility="hidden";
	}
}
