 // Hide all filter sections initially
 $(".filter-section").hide();

 // Toggle filter sections on clicking the heading
 $(".filter-heading").click(function () {
     $(this).next(".filter-section").slideToggle("fast");
     $(this).find(".icon").toggleClass("rotate-180");
 });

  // Open filter sidebar
$('.filter-btn').on('click', function(){
    $('.filter-mobile').removeClass('-translate-x-full').addClass('translate-x-0');
    $('.filter-overlay').removeClass('hidden');
});

// Close filter sidebar
$('.hide-filter').on('click', function(){
    $('.filter-mobile').removeClass('translate-x-0').addClass('-translate-x-full');
    $('.filter-overlay').addClass('hidden');

});