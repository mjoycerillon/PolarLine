$(function() {
    // Call the Window On Load Function
    $(window).on('load', function () {
        var cartSubTotal = 0.0;
        $('.cartSubTotal').each(function(){
            cartSubTotal += parseFloat($(this).text().substr(1));
            $('#txtCartSubTotal').text("$"+cartSubTotal.toFixed(2));
            $('#txtCartTotal').text("$"+cartSubTotal.toFixed(2))
        });

        $('.cart-minus').on('click', function() {
            var currentQuantity = $(this).parents('.cartItem').find('.cartItemQuantity').val();
            if (currentQuantity > 0) {
                $(this).parents('.cartItem').find('.cartItemQuantity').val(parseInt(currentQuantity) - 1);
                updateItemSubtotal($(this));
            }
        });

        $('.cart-add').on('click', function() {
            var currentQuantity = $(this).parents('.cartItem').find('.cartItemQuantity').val();
            $(this).parents('.cartItem').find('.cartItemQuantity').val(parseInt(currentQuantity) + 1);
            updateItemSubtotal($(this));
        });

        function updateItemSubtotal(element){
            var itemPrice = $(element).parents('.cartItem').find('.cartItemPrice').text().substr(1);
            var itemQuantity = $(element).parents('.cartItem').find('.cartItemQuantity').val();
            var subTotal = parseFloat(itemPrice) * parseFloat(itemQuantity);
            var currentSubTotal = parseFloat($(element).parents('.cartItem').find('.cartSubTotal').text().substr(1));
            var cartSubTotal = (parseFloat($('#txtCartSubTotal').text().substr(1)) - currentSubTotal) + subTotal;
            $(element).parents('.cartItem').find('.cartSubTotal').text('$'+ subTotal.toFixed(2));
            $('#txtCartSubTotal').text("$"+cartSubTotal.toFixed(2));
            $('#txtCartTotal').text("$"+cartSubTotal.toFixed(2))
        }

        $('.removeItem').on('click', function() {
            var element = $(this).parents('.cartItem');
            var price = $(this).parent().next().find('.cartSubTotal').text().substr(1);
            var cartSubTotal = parseFloat($('#txtCartSubTotal').text().substr(1)) - parseFloat(price);
            $('#txtCartSubTotal').text("$"+cartSubTotal.toFixed(2));
            $('#txtCartTotal').text("$"+cartSubTotal.toFixed(2))

            element.animate({opacity: '0'}, 150, function(){
                element.animate({height: '0px'}, 150, function(){
                    element.remove();
                });
            });
        });
    });
});