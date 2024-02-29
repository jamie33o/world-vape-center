$(document).ready(function(){
    // Select the element with class 'account-modal-title'
    const modelTitle = $('.account-modal-title');

    // Attach a click event handler to elements with class 'toggle-form'
    $('.toggle-form').click(function(){
        // Toggle the visibility of all elements with class 'form'
        $('.form').each(function(){
            $(this).toggleClass('d-none');
        });

        // Change the text content of the element with class 'account-modal-title'
        // based on its current text content
        if (modelTitle.text() ===  'Sign In') {
            modelTitle.text('Sign Up');
        } else {
            modelTitle.text('Sign In');
        }
    });
});
