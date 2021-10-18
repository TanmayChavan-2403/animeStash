
function navigate(){
    window.scrollTo(0, 800);
}

document.addEventListener('scroll', parallax)

function parallax(){
	var initialVAl = 350;
	var scrollVal = window.scrollY;
	const genres = document.querySelector('.genres');
	var val = scrollVal/4;

	genres.style.transform = `translateY(${val}px)`;
	document.documentElement.style.setProperty('--o', scrollVal/9 +'%');
}


function pushDown(){
    var cont1 = document.querySelector('.arrowCont1');
    var cont2 = document.querySelector('.arrowCont2');
    var cont3 = document.querySelector('.arrowCont3');
    var temp1;
    var temp2;
    setInterval(function(){        
        cont1.style.opacity = '100%'; //cont3
        cont2.style.opacity = '50%'; //cont1
        cont3.style.opacity = '30%'; //cont2
        // console.log('values are', cont1, cont2, cont3);
        
        temp1 = cont1;
        temp2 = cont2;

        cont2 = cont3;
        cont1 = temp2; 
        cont3 = temp1;       
        
    }, 250);
    
} 

