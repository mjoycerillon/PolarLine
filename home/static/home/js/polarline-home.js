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

    // Upon clicking the button Shop Now, the page will redirect to Shop Page
    $('#btnHomeShopNow').click(function(){
        window.location = "shop"
    });

    // Upon clicking the button Shop Now, the page will redirect to Shop Page
    $('.promo-image').click(function(){
        window.location = "shop"
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

