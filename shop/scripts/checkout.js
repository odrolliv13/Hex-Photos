$(function() {
		$('.title').each(function(){
		$(this).css({'color': 'red'})
	});
	$('.active').mouseover(function(){
		$(this).css('text-decoration', 'underline');
	});
	$('.active').mouseout(function(){
		$(this).css('text-decoration', 'none');
	});
});