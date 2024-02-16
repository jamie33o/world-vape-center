$(document).ready(function () {
    $('#mob-search-input').on('click', function(){
        $('#search-form').removeClass('d-none')
    })
    $('.close-search').click(() => $('#search-form').addClass('d-none'))

    $(".search-btn").on("click", function () {
        $("#search-form").toggleClass("d-none");
    });

    $('#search-form').submit(function(event) {
        event.preventDefault();
        search();
    });

    $('#search-form input').on('input', function() {
        search();
    });

    function search() {
        var query = $('#search-input').val();
        var formAction = $('#search-form').attr('action');

        $.ajax({
            url: formAction,
            type: 'GET',
            data: {q: query},
            success: function(data) {
                
                const $cartContainer = $('.results');
                $cartContainer.empty()
                const product = data.products;
                if(product.length > 0){
                    $('.results-container').removeClass('d-none')
                  }else{
                    $('.results-container').addClass('d-none')
                  }
                // Loop through the cart items and create HTML content
                product.forEach(item => {
                  const itemHTML = `
                  <a href="${item.url}" class="text-decoration-none">
                    <div class="card mb-4 border rounded p-3">
                        <div class="d-flex flex-dir-row">
                            <img src="${item.img}" alt="${item.name}" class="img-fluid rounded-start mr-3" width="50">
                            <div class="card-body p-0">
                                <p class="card-title">${item.name}</p>
                                <p class="card-text"><strong>${item.price}</strong></p>
                            </div>
                        </div>
                    </div>
                </a>
                  `;
              
                  // Append the item HTML to the cart container using jQuery
                  $cartContainer.append(itemHTML); 
                  
                });             
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    $('.like-form').submit(function (e) {
        e.preventDefault(); // Prevent the form from submitting normally
    
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(), // Serialize the form data
            success: function (response) {
                console.log(response)
                $('.messages').remove()
               const message = $(`
               <div class="row justify-content-end m-0 messages">
                <div class="mr-5">
                    <div class="alert bg-light mx-auto border-dark">
                        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">
                            ×</button> 
                        <strong>${response.status}</strong>
                        <hr class="message-inner-separator">
                        <p>
                          ${response.message}</p>
                    </div>
                </div>
              </div>`)
              $('main').append(message)        
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
