/*
toggleable show more and show less
system where the show less and addictional
content are nested inside a hidden class
where it is the next element
*/
$(document).ready(function(){
	$('.read-more').on('click',function(){
		$(this).addClass('hide')
		$(this).next().removeClass('hide');
	})

	$('.read-less').on('click',function(){
		$(this).parent().addClass('hide')
		$(this).parent().prev().removeClass('hide')

	})
})