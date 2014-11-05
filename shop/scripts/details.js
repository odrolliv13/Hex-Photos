$(function (){
       
       $('#content img').mouseover(function(){
          $(this).css("cursor","pointer");
          $(this).animate({width: "300px"}, 'slow');
       });
    
    $('#content img').mouseout(function(){   
          $(this).animate({width: "200px"}, 'slow');
    });
});


// $(function (){
// 	$('#content img').hover(function(){
// 		$(this).animate({width:"100%",height:"100%"
// 		}, 'slow');
// 	};
// 			function(){
// 				$(this).animate({width:"50%",height:"50%"}, 'slow');   
// 			});
// });