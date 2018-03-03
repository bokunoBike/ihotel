var myChart = echarts.init(document.getElementById('showChart'),'dark');

//监控标签页的打开和隐藏
document.addEventListener('webkitvisibilitychange',function()
			 {
					 if(document.webkitVisibilityState=='hidden')
					 {}
					 else
					 {
							 $.ajax(getting);
					 }
			 })
document.addEventListener('mozvisibilitychange',function()
			 {
					 if(document.mozVisibilityState=='hidden')
					 {}
					 else
					 {
							 $.ajax(getting);
					 }
			 })

 //长轮询参数获取房间状态是否改变
 var getting =
 {
 	url:'!!!',//后边再改!!!
 	dataType:'json',
 	success:function(res)
 	{
 		console.log(res);
 		//修改提示信息
    var noticeWords=document.getElementById('noticesWord');
    if(noticeWords=='当前房间内有人')
    {
      document.getElementById('noticesImg').src='http://localhost:3000/images/homeOut.png';
      document.getElementById('noticesWord').innerHTML='当前房间内无人';
      document.getElementById('notice').innerHTML='<p id="noticeWord"><img id="noticeImg" src="http://localhost:3000/images/homeOut.png" alt="" class="pull-left"/>当前房间内无人</p>'
    }
    else
    {
      document.getElementById('noticesImg').src='http://localhost:3000/images/home.png';
      document.getElementById('noticesWord').innerHTML='当前房间内有人';
      document.getElementById('notice').innerHTML='<p id="noticeWord"><img id="noticeImg" src="http://localhost:3000/images/home.png" alt="" class="pull-left"/>当前房间内有人</p>'
    }
    $.ajax(getting);
 	},
 	error:function(res)
 	{
 		$.ajax(getting);
 	}
 }

//获取随机数据
function randomData() {
    now = new Date(+now + 1000);
    var year=now.getFullYear();
    var month=now.getMonth()+1;
    var day=now.getDate();
    var hour=now.getHours();
    var minute=now.getMinutes();
    var second=now.getSeconds();
    value = value + Math.random() * 21 - 10;
    return {
        name: now.toString(),
        value: [
            year+'/'+month+'/'+day+' '+hour+':'+minute+':'+second,
            Math.round(value)
        ]
    }
}

var data = [];
var now = new Date()-17*60*1000;
var oneDay = 24 * 3600 * 1000;
var value = Math.random() * 1000;
for (var i = 0; i < 1000; i++) {
    data.push(randomData());
}

option = {
    title: {
        text: '传感器输出信号',
        textStyle: {
               fontWeight: 'normal',              //标题颜色
               //color: 'gray'
           },
    },
    tooltip: {
        trigger: 'axis',
        formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return date.getHours() + ':' + date.getMinutes() + ':' + date.getSeconds() + ' value: ' + params.value[1];;
        },
        axisPointer: {
            animation: false
        }
    },
    xAxis: {
        type: 'time',
        splitLine: {
            show: false
        }
    },
    yAxis: {
        type: 'value',
        boundaryGap: [0, '100%'],
        splitLine: {
            show: false
        }
    },
    backgroundColor:'#303030',
    series: [{
        smooth:true,
        name: '模拟数据',
        type: 'line',
        showSymbol: false,
        hoverAnimation: false,
        data: data
    }]
};

setInterval(function () {

    for (var i = 0; i < 1; i++) {
      //myChart.clear();
        data.shift();
        data.push(randomData());
    }

    myChart.setOption(option);
}, 1000);

$(document).ready(function(){
  $('#changeRoom').click(function(){
    document.getElementById('form').style.display="block";
    document.getElementById('showChart').style.display="none";
    windowsHeight = document.documentElement.clientHeight;
    totalHeight=document.getElementById("none").offsetTop;
    if(totalHeight<windowsHeight)
    {
      colHeight = windowsHeight-document.getElementById("footer").offsetTop;
      document.getElementById("footer").style.height=colHeight+"px";
    }
  });
  $('.form button').click(function(){
    var windowWidth=document.documentElement.clientWidth;
    if(windowWidth<768)
    {
      document.getElementById('form').style.display="none";
      document.getElementById('showChart').style.display="block";
    }
  });
});
