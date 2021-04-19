$(function() {
    /**
     * Navigation Links
     */
    // Upon hover on the Account Icon, a drop-down should be displayed on the screen
    $("#navAccount").hover(function () {
        $(this).children('ul').stop(true, false, true).slideToggle(400);

    });

    // Upon hover on Shop, a sub-menu should be displayed on the screen.
    $('#navShop').hover(function() {
        if (!$('.burger').is(":visible")) {
            $(this).children('div').stop(true, false, true).slideToggle(400);
        }
    });

    $('.burger-container').on('click', function() {
        $('.nav-links-grp').children('ul').toggle('slide', {
            direction: 'left'
        }, 1000);
    });
});
