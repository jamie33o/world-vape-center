$(".fav-form").submit(function (event) {
    event.preventDefault(); // Prevent default form submission

    $.ajax({
        type: "POST",
        url: $(this).attr("action"),
        data: $(this).serialize(), // Serialize form data
        success: function (response) {
            location.reload();
        },
        error: function (xhr, status, error) {
            location.reload();
        }
    });
});
