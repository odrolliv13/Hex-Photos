$(function() {
	$('.thumbnail').mouseover(function(){
		$(this).css('border', '5px solid gray');
	});
	$('.thumbnail').mouseout(function(){
		$(this).css('border', 'none');
	})
});