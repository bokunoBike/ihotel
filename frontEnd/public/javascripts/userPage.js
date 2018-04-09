var systemPersonNumber;//系统检测的人数，从后端获取！！！
var nowPerson ;
var changeNumber;
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
	ws.onclose = function()
	{
		ws.send(0);
	}
	ws.onerror = function(e)
	{
		ws.send(0);
	}
}
//小屏幕点击显示房间状态按钮
function showStatus()
{
	var select = document.getElementById('select');
	var statusWindow = document.getElementById('main-window');
	select.style.display='none';
	statusWindow.style.display='block';
}
//小屏幕点击返回按钮
function backSelect()
{
	document.getElementById('select').style.display = 'block';
	document.getElementById('main-window').style.display = 'none';
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
//发送报错信息
function sendCorrect()
{
	document.getElementById('cancel').style.display = 'none';
	if((systemPersonNumber == changeNumber)||(clickChange == false))
	{
		document.getElementById('myModalBody').innerHTML = '您报告的人数与系统检测人数一致!';
	}
	else
	{
		document.getElementById('myModalBody').innerHTML = '信息已发送，请等待审核!';
	}
	document.getElementById('number').innerHTML = systemPersonNumber;
	getPersonNumber();
}
//设置为被动模式
function setModalText()
{
	document.getElementById('cancel').style.display = 'inline-block';
	document.getElementById('myModalBody').innerHTML = '房间将于您离开后立即断电！'
}
$('#myModal').on('show.bs.modal', function () {
	document.getElementsByTagName('body')[0].style.paddingTop='0';
	document.getElementById('navbarContainer').style.position='static';
})
$('#myModal').on('hidden.bs.modal', function () {
	document.getElementsByTagName('body')[0].style.paddingTop='75px';
  document.getElementById('navbarContainer').style.position='fixed';
})
