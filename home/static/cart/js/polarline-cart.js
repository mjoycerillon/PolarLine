$(function() {
    var isLoggedOn = localStorage.getItem("isLoggedOn");
    var accounts = localStorage.getItem("accounts");
    var userData = localStorage.getItem("current_user");
    var user = JSON.parse(userData);

    // Call the Window On Load Function
    $(window).on('load', function () {
        var guest_user = localStorage.getItem("guest_user");
        var cart = JSON.parse(guest_user);
        if (isLoggedOn == "true") {
            cart = user["cart"];
        }

        loadCart(cart);

        $('.cart-minus').on('click', function() {
            var currentQuantity = $(this).siblings('.cartItemQuantity').val();
            if (currentQuantity > 0) {
                $(this).siblings('.cartItemQuantity').val(parseInt(currentQuantity) - 1);
				var cartItemId = $(this).siblings('.cartItemQuantity').data("cart-id");
                var cartItemSubtotal = $(this).siblings('.cartItemQuantity').data("sub-total-id");
                updateItemSubtotal($(this), cartItemId, cartItemSubtotal);
            }
        });

        $('.cart-add').on('click', function() {
            var currentQuantity = $(this).siblings('.cartItemQuantity').val();
            $(this).siblings('.cartItemQuantity').val(parseInt(currentQuantity) + 1);
            var cartItemId = $(this).siblings('.cartItemQuantity').data("cart-id");
            var cartItemSubtotal = $(this).siblings('.cartItemQuantity').data("sub-total-id");
            updateItemSubtotal($(this), cartItemId, cartItemSubtotal);
        });

        function updateItemSubtotal(element, cartItemId, cartItemSubtotalId){
            var itemPrice = $(element).parents().find('#'+cartItemId).text().substr(1);
            var itemQuantity = $(element).siblings('.cartItemQuantity').val();
            var subTotal = parseFloat(itemPrice) * parseFloat(itemQuantity);
            var currentSubTotal = parseFloat($(element).parents('.cartItem').find('.cartSubTotal').text().substr(1));
            var cartSubTotal = (parseFloat($('#txtCartSubTotal').text().substr(1)) - currentSubTotal) + subTotal;
            $(element).parents().find('#'+cartItemSubtotalId).text('$'+ subTotal.toFixed(2));
            $('#txtCartSubTotal').text("$"+cartSubTotal.toFixed(2));
            $('#txtCartTotal').text("$"+cartSubTotal.toFixed(2))

        }

        function emptyCart() {
            var card =
                '<div class="card mb-2" style="width: 90%;">' +
                    '<div class="card-body">' +
                        '<div class="row justify-content-center align-items-center" style="height: 403px;">' +
                            '<div class="row w-50">' +
                                '<img class="img-fluid" src="/static/cart/images/cart-empty.png" alt="" height="50px">' +
                            '</div>' +
                            '<div class="row justify-content-center fw-bolder" style="font-size: 20px;">You have no items in your shopping cart.</div>' +
                        '</div>' +
                    '</div>' +
                '</div>'
                $("#cartContainer").append(card);

        }

        function loadCart(cart) {
            var cartSubTotal = 0.0;
            if (cart != null) {
                for (i = 0; i < cart.length; i++) {
                    var productName = "";
                    var productPrice = "";
                    var productQuantity = "";
                    var productImage = "";
                    var cartItemSubTotal = 0.0;
                    $.each(cart[i], function(key, value) {
                         switch(key) {
                            case "product":
                                productName = value;
                                break;
                            case "price":
                                productPrice = value;
                                break;
                            case "quantity":
                                productQuantity = value;
                                break;
                            case "imageLocation":
                                productImage = value;
                                break;
                          }
                    });
                    cartItemSubTotal = productPrice * productQuantity;
                    cartSubTotal += cartItemSubTotal;
                    var card =
                          '<div class="row pb-1 justify-content-center cartItem">' +
                              '<div class="card mb-2" style="width: 90%;">' +
                                  '<div class="card-body">' +
                                      '<div class="row d-flex justify-content-end">' +
                                          '<button type="button" class="btn-close removeItem" aria-label="Close"></button>' +
                                      '</div>' +
                                      '<div class="row">' +
                                          '<div class="col"><img src="'+ productImage +'" class="img-fluid img-thumbnail"></div>' +
                                          '<div class="col align-items-center text-center fw-bolder">'+ productName +'</div>' +
                                          '<div class="col align-items-center">' +
                                              '<div class="container">' +
                                                  '<div class="row justify-content-center">Price</div>' +
                                                  '<div id="cartItemPrice' + i + '" class="row justify-content-center text-danger fw-bolder">$'+ productPrice +'</div>' +
                                              '</div>' +
                                          '</div>' +
                                          '<div class="col align-items-center">' +
                                              '<div class="container p-0">' +
                                                  '<div class="row justify-content-center">Quantity</div>' +
                                                  '<div class="row justify-content-center">' +
                                                      '<div class="input-group justify-content-center text-center">' +
                                                          '<button class="cart-minus input-group-text">-</button>' +
                                                          '<input class="form-control cartItemQuantity" type="number" data-cart-id="cartItemPrice'+ i +'" data-sub-total-id="cartItemSubtotal' + i +'" value="'+ productQuantity +'">' +
                                                          '<button class="cart-add input-group-text">+</button>' +
                                                      '</div>' +
                                                  '</div>' +
                                              '</div>' +
                                          '</div>' +
                                          '<div class="col align-items-center">' +
                                              '<div class="container">' +
                                                  '<div class="row justify-content-center">Total</div>' +
                                                  '<div id="cartItemSubtotal' + i + '" class="cartSubTotal row justify-content-center text-danger fw-bolder">$'+ cartItemSubTotal +'</div>' +
                                              '</div>' +
                                          '</div>' +
                                      '</div>' +
                                  '</div>' +
                              '</div>' +
                          '</div>';
                    $('#cartContainer').append(card);
                }
            } else {
                emptyCart();
            }

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

            if (cartSubTotal == 0.0) {
                emptyCart();
            }
        });
    });
});