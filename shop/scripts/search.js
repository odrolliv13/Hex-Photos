$(function() {
		$('.title').each(function(){
		$(this).css({'color': 'red'})
	});
	$('.thumbnail').mouseover(function(){
		$(this).css('fontWeight', '900');
	});
	$('.thumbnail').mouseout(function(){
		$(this).css('fontWeight', '200');
	});
});