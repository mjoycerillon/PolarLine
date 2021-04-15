$(function() {
    $(window).on('load', function () {
        AOS.init();
    });

    $('.shop-product').click(function(){
        var imgLoc = $(this).children('img').attr('src');
        var prodTitle = $(this).children('.shop-product-name').text();
        var prodPrice = $(this).children('.shop-product-cost').text().substr(1,$(this).children('.shop-product-cost').text().length);
        var prodTitleParts = $(this).children('.shop-product-name').text().split(' ');
        
        var color = prodTitleParts[prodTitleParts.length-2].slice(1,prodTitleParts[prodTitleParts.length-2].length-1);
        console.log(color);
        localStorage.setItem("prod_color",color);
        localStorage.setItem("img_loc",imgLoc);
        localStorage.setItem("prod_title",prodTitle);
        localStorage.setItem("prod_cost",prodPrice);
        window.location.href="details.html";
        var fromShopPage = true;
        localStorage.setItem("fromShopPage",fromShopPage);
    });

    $('.overlayButton').click(function(e){
    e.stopPropagation();
    //e.preventDefault();
    var isLoggedOn = localStorage.getItem("isLoggedOn");
    //console.log(isLoggedOn);
    var accounts = localStorage.getItem("accounts");

    var accountsObj = JSON.parse(accounts);
    //console.log(localStorage.getItem("current_user"));
    console.log('button clicked');
    swal("Success!", $(this).parent().children('.shop-product-name').text()+ " is added to bag.", "success");
    //console.log(accountsObj[0]["cart"]);
    if(isLoggedOn == "true")
    {
    var currentUser = JSON.parse(localStorage.getItem("current_user"));
    currentUser["cart"].push(
        {
            "imageLocation" : $(this).parent().children('img').attr('src'),
            "price" : $(this).parent().children('.shop-product-cost').text().substr(1,$(this).parent().children('.shop-product-cost').text().length), 
            "product" : $(this).parent().children('.shop-product-name').text(),
            "quantity" : "1"
        }
    );
    accountsObj[0]["cart"].push(
        {
            "imageLocation" : $(this).parent().children('img').attr('src'),
            "price" : $(this).parent().children('.shop-product-cost').text().substr(1,$(this).parent().children('.shop-product-cost').text().length),  
            "product" : $(this).parent().children('.shop-product-name').text(),
            "quantity" : "1"
        }
    );
    //console.log(accountsObj[0]);
    accounts = JSON.stringify(accountsObj);
    var currUser = JSON.stringify(currentUser);
    localStorage.setItem("current_user",currUser);
    localStorage.setItem("accounts",accounts);
    }
    else{
        var guestObj = localStorage.getItem("guest_user");
        if (guestObj == null) {
            guestObj = [];
            localStorage.setItem("guest_user",JSON.stringify(guestObj));
            guestObj = localStorage.getItem("guest_user");
        }
        guest = JSON.parse(guestObj);
        guest.push(
            {
            "imageLocation" : $(this).parent().children('img').attr('src'),
            "price" : $(this).parent().children('.shop-product-cost').text().substr(1,$(this).parent().children('.shop-product-cost').text().length), 
            "product" : $(this).parent().children('.shop-product-name').text(),
            "quantity" : "1"
            }
        );
        var guestUser = JSON.stringify(guest);
        localStorage.setItem("guest_user",guestUser);
        console.log(localStorage.getItem("guest_user"));
    }
    });
});