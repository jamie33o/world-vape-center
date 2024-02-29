$(document).ready(function () {
    // Handle click event on the mobile search input
    $('#mob-search-input').on('click', function(){
        $('#search-form').removeClass('d-none');
    });

    // Handle click event on the close-search button
    $('.close-search').click(() => $('#search-form').addClass('d-none'));

    // Handle click event on the general search button
    $(".search-btn").on("click", function () {
        $("#search-form").toggleClass("d-none");
    });

    // Handle form submission for the search form
    $('#search-form').submit(function(event) {
        event.preventDefault();
        search();
    });

    // Handle input event on the search input field
    $('#search-form input').on('input', function() {
        search();
    });

    // Define the search function
    function search() {
        var query = $('#search-input').val();
        var formAction = $('#search-form').attr('action');

        $.ajax({
            url: formAction,
            type: 'GET',
            data: {q: query},
            success: function(data) {
                const $cartContainer = $('.results');
                $cartContainer.empty();
                const product = data.products;
                if(product.length > 0){
                    $('.results-container').removeClass('d-none');
                } else {
                    $('.results-container').addClass('d-none');
                }

                // Loop through the products and create HTML content
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

    // Handle form submission for the like-form
    $('.like-form').submit(function (e) {
        e.preventDefault(); // Prevent the form from submitting normally

        const $favouriteCard = $(this).closest('.fav-card');
    
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(), // Serialize the form data
            success: function (response) {
                console.log(response);
                $('.messages').remove();
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
                if ($favouriteCard) {
                    $favouriteCard.remove();
                }      
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
