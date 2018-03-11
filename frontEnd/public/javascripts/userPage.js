$('#myModal').on('show.bs.modal', function () {
	document.getElementsByTagName('body')[0].style.paddingTop='0';
	document.getElementById('navbarContainer').style.position='static';
})
$('#myModal').on('hidden.bs.modal', function () {
	console.log(document.getElementById('navbarContainer').clientHeight);
	document.getElementsByTagName('body')[0].style.paddingTop='75px';
  document.getElementById('navbarContainer').style.position='fixed';
})
