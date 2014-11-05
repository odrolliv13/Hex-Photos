
$(function(){
	$('#login_button').off('click.login').on('click.login', function(){
		$('body').loadmodal({
			id: 'login_modal',
			title: 'Login',
			url: '/shop/loginmodal/',
		});
	});
});

$(function(){
	$('#new_account').off('click.create').on('click.create', function(){
		$('body').loadmodal({
			id: 'new_account',
			title: 'Create an Account',
			url: '/shop/new_account/',
		});
	});
});
