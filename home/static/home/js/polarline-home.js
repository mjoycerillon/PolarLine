$(function() {

    // Upon mouse enter the image will apply the class filter
    $('.promo-image').mouseenter(function() {
        $(this).toggleClass("filter");
        $(this).css("cursor", "pointer");
    });

    // Upon mouse leave the image will remove the class filter
    $('.promo-image').mouseleave(function() {
        $(this).toggleClass("filter");
    });

    // Calling the plugin Owl Carousel
    $('.owl-carousel').owlCarousel({
        stagePadding: 0,
        autoplay:true,
        autoplayTimeout:5000,
        animateOut: 'fadeOut',
        items:1,
        loop:true,
        responsiveClass:true
    });

});

