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

    $('.carousel').carousel({
        interval: 5000,
        ride: 'carousel'
    })

});

