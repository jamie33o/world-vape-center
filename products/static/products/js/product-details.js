$(document).ready(function(){

  var reviewBox = $('#post-review-box');
  var newReview = $('#new-review');
  var openReviewBtn = $('#open-review-box');
  var closeReviewBtn = $('#close-review-box');
  var ratingsField = $('#ratings-hidden');

  openReviewBtn.click(function (e) {
      e.preventDefault();
      reviewBox.removeClass('d-none');
      reviewBox.slideDown(400, function () {
        $('#new-review').trigger('autosize.resize');
        newReview.focus();
    });
      openReviewBtn.fadeOut(100);
      closeReviewBtn.show();
      addStars('#post-review-box');
  });

  closeReviewBtn.click(function (e) {
      e.preventDefault();
      reviewBox.slideUp(300, function () {
          newReview.focus();
          openReviewBtn.fadeIn(200);
      });
      closeReviewBtn.hide();
      $('.starrr i').remove();
  });

  $('.starrr').on('starrr:change', function (e, value) {
      ratingsField.val(value);
  });

  function addStars(parent) {
    for(let i = 1; i < 6; i++){
      $(`${parent} .starrr`).append(`<i value="${i}" class="fa-regular fa-star"></i>`);
    }

    $(`${parent} .starrr i`).on('mouseover', function(){
      for(let x=0; x <= $(this).attr('value'); x++){
      $(`${parent} .starrr i[value=${x}]`).removeClass('fa-regular').addClass('fa-solid');
      }
    });
    
    $(`${parent} .starrr i`).on('mouseout', function(){
      $(`${parent} .starrr i`).each(function(){
        $(this).removeClass('fa-solid').addClass('fa-regular');
      });
    });
    $(`${parent} .starrr i`).on('click', function(){
      $(`${parent} .starrr i`).off();
      $(`${parent} #ratings-hidden`).val($(this).attr('value'));
    });

  }

  $(document).on('submit', '.review-form', function(e) {
        e.preventDefault();

        // Serialize form data
        var formData = $(this).serialize();
        
        // Send AJAX request
        $.ajax({
            type: 'POST',
            url: $(e.target).data('url'),  // Replace with the correct URL
            data: formData,
            success: function(response) {
              location.reload();

            },
            error: function(response) {
                // Handle error response
                console.log(response);
                // You can display error messages or handle form errors here
            }
        });
    });


  $(document).on('click', '.delete-review', function(e) {
      e.preventDefault();

      let review_card = $(this).closest('.row');
      let csrfToken = $(this).data('csrf');
      $('.modal-backdrop').removeClass('show');
        $.ajax({
          type: 'DELETE',
          url: $(e.target).data('url'),
          headers: {
            'X-CSRFToken': csrfToken,
          },
          
          success: function(response) {
            setTimeout(() => {
              review_card.remove();
            }, 1000);    
          },
          error: function(response) {
              // Handle error response
              console.log(response);
              // You can display error messages or handle form errors here
          }
      });
  });

  $(document).on('click', '.edit-btn', function(e) {
    addStars('#edit-modal');
});


  $(document).on('click', '.custom-radio', function(){
    $('.cur_choice').text($(this).find('input').val());
  } );

});