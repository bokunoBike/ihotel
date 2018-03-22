windowsHeight = document.documentElement.clientHeight;
totalHeight=document.getElementById("none").offsetTop;

if(totalHeight<windowsHeight)
{
  colHeight = windowsHeight-document.getElementById("footer").offsetTop;
  document.getElementById("footer").style.height=colHeight+"px";
}
//注释掉!!!
$(document).ready(function(){
  $(window).resize(function(){
    //location.reload();
  });
});
