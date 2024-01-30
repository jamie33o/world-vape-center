$(document).ready(function(){
        
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();
        let chosenOption = $('.options input:checked').val();
        let csrf = $(this).data('csrf')
        let url = $(this).data('url')

        let qty = $("#select" + $(e.target).val() + " option:selected").text() 
        
        if(!qty)
            qty = 1

        $.ajax({
            type: "POST",
            url: url,
            headers: {
                'X-CSRFToken': csrf
            },
            data: {
                product_id: $(e.target).val(),
                product_quantity: qty,
                product_choice: chosenOption ? chosenOption : null,
            },
    
            success: function (json) {
                $(".cart-qty").text(json.qty);
                $(".cart-total").text('€ '+ json.cart_total);
            },
    
            error: function (xhr, errmsg, err) {
                console.log(err)
            },
        });
    });
})
