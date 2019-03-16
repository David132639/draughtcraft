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