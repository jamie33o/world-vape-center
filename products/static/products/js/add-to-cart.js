$(document).ready(function(){
        
    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: $(e.target).data('url'),
            data: {
                product_id: $(e.target).val(),
                product_quantity: "1",
                csrfmiddlewaretoken: $(e.target).data('csrf'),
                action: "post",
            },
    
            success: function (json) {
                $(".cart-qty").text(json.qty);
                $(".cart-total").text('€ '+ json.cart_total);
            },
    
            error: function (xhr, errmsg, err) {},
        });
    });
})
