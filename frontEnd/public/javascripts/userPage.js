const text = document.querySelector('.text')
const svg = document.querySelector('svg')

const support = 'd' in text.style


if (!support) {

// 	bring text in center
	text.classList.add('center')

// 	blur svg element
	svg.classList.add('blur')
}

var numOfPeople =1;

if(numOfPeople == 1)
	{
		svg.setAttribute('d','M0,0 L50,0 L50,50 L50,100 L0,100 L0,25 L0,0')
	}

$('#myModal').on('show.bs.modal', function () {
	document.getElementsByTagName('body')[0].style.paddingTop='0';
	document.getElementById('navbarContainer').style.position='static';
})
$('#myModal').on('hidden.bs.modal', function () {
	console.log(document.getElementById('navbarContainer').clientHeight);
	document.getElementsByTagName('body')[0].style.paddingTop='75px';
  document.getElementById('navbarContainer').style.position='fixed';
})
