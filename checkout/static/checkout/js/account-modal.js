$(document).ready(function(){
    const modelTitle = $('.account-modal-title')
    $('.toggle-form').click(function(){
        $('.form').each(function(){

            $(this).toggleClass('d-none');
        });
        if (modelTitle.text() ===  'Sign In') {
            modelTitle.text('Sign Up');
        } else {
            modelTitle.text('Sign In');
        }
    });
});
