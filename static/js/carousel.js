
$(document).ready(function () {
    let currentIndex = 0;
    const slides = $("#carousel-inner .carousel-slide");
    const cardsPerslide = window.innerWidth >= 1024 ? 3 : window.innerWidth >= 640 ? 2 : 1; // lg:3, sm:2, mobile:1
    
    const totalSlides = slides.length % cardsPerslide === 0 ? slides.length / cardsPerslide : Math.floor(slides.length / cardsPerslide) + 1;

    function showSlide(index) {
        let newTransform = `translateX(-${index * 100}%)`;
        $("#carousel-inner").css("transform", newTransform);
    }

    $("#nextBtn").click(function () {
        currentIndex = (currentIndex + 1) % totalSlides;
        showSlide(currentIndex);
    });

    $("#prevBtn").click(function () {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        showSlide(currentIndex);
    });

    // Auto-slide every 5 seconds
    // setInterval(() => {
    //     currentIndex = (currentIndex + 1) % totalSlides;
    //     showSlide(currentIndex);
    // }, 5000);
});
