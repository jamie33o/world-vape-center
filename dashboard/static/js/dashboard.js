$('#status-form').submit(function(e){
    e.preventDefault()
    let form = $(this)
    let formData = $(this).serialize()
    const url = $(this).attr('action')
    let id = url.substring(url.lastIndexOf('/') + 1);

    $.ajax({
        url: url,  
        method: 'POST',                
        data: formData,
        success: function(response) {  
            const message = $(`
                <div class="row justify-content-end m-0 messages">
                    <div class="mr-5">
                        <div class="alert bg-light mx-auto border-dark">
                            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">
                                ×</button> 
                            <strong>${response.status}</strong>
                            <hr class="message-inner-separator">
                            <p>${response.message}</p>
                        </div>
                    </div>
                </div>
            `);
            $('main').append(message);
                setTimeout(() => {
                  $(message).remove()
                }, 3000); 

            $(`#status${id}`).text(form.find('[name="status"]').val())
        },
        error: function(xhr, status, error) {  
            $('.messages').remove();

            const message = $(`
                <div class="row justify-content-end m-0 messages">
                    <div class="mr-5">
                        <div class="alert bg-light mx-auto border-dark">
                            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">
                                ×</button> 
                            <strong>${status}</strong>
                            <hr class="message-inner-separator">
                            <p>${error}</p>
                        </div>
                    </div>
                </div>
            `);
            $('main').append(message);
            setTimeout(() => {
              $(message).remove()
            }, 3000); 
        }
    });
});
