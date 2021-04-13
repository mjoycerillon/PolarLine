$(function() {
    // Call the Window On Load Function
    $(window).on('load', function () {
        var cartSubTotal = 0.0;
        $('.cartSubTotal').each(function(){
            cartSubTotal += parseFloat($(this).text().substr(1));
            $('#txtCartSubTotal').text("$"+cartSubTotal.toFixed(2));
            $('#txtCartTotal').text("$"+cartSubTotal.toFixed(2))
        });

        $('.removeItem').on('click', function() {
            element.animate({opacity: '0'}, 150, function(){
                element.animate({height: '0px'}, 150, function(){
                    element.remove();
                });
            });
        });
    });
});