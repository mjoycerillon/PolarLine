$(function() {
    // Global variables
    var isLoggedOn = localStorage.getItem("isLoggedOn");
    var accounts = localStorage.getItem("accounts");
    var userData = localStorage.getItem("current_user");
    var user = JSON.parse(userData);

    // Call the Window On Load Function
    $(window).on('load', function () {
        // Validate if dummy data exists on the local storage
        if (accounts == null) {
            var accounts = 
            [{
                "first_name": "Rachel Karen",
                "last_name": "Green",
                "email": "rachelgreen@gmail.com",
                "password": "polar",
                "billing_address": "1457 London Rd, Sarnia, Ontario Canada, N7S 6K4",
                "shipping_address": "1457 London Rd, Sarnia, Ontario Canada, N7S 6K4",
                "birth_date": "09/22/1994",
                "cart": []

            }];
            var accountsJSON = JSON.stringify(accounts);
            localStorage.setItem("accounts", accountsJSON);
        } 

        if (isLoggedOn == "true") {
            $("#navAccountName").text(user["first_name"]);
            $(".nav-account-d-menu").append('<li><a id="navSignOutLink" class="dropdown-item" href="index.html">Sign Out</a></li>')
            $(".navAccountLink").attr( "href", "account.html");
        }
    });

    /**
     * Navigation Links
     */
    // Upon clicking the account icon, if the user already logged on, Account Page should be displayed
    $('#navAccount').on('click', function() {
        if (isLoggedOn == "true") {
            $(this).attr( "href", "account.html");
        }
    });

    // Upon hover on the Account Icon, a drop-down should be displayed on the screen
    $("#navAccount").hover(function () {
        $(this).children('ul').stop(true, false, true).slideToggle(400);

    });

    // Upon hover on Shop, a sub-menu should be displayed on the screen.
    $('#navShop').hover(function() {
        $(this).children('div').stop(true, false, true).slideToggle(400);
    });


    $(document).on('click', '#navSignOutLink', function() {
        localStorage.setItem("isLoggedOn", "false");
        localStorage.removeItem("current_user");
        $('#navSignOutLink').remove(); // when referencing by id
    }); 


    /**
     * Login
     */
    // Upon login, save the data of the user to local storage
    $('#loginForm').on('submit', function(event) {

        // Get value of Login Email and Password
        var loginEmail = $('#txtLoginEmail').val();
        var loginPassword = $('#txtLoginPassword').val();

        // Retrieve the data from the local storage and parse it
        var loginData = localStorage.getItem("accounts");
        var objectData = JSON.parse(loginData);
        var emailFound = false;

        // Find the account and save it into global variable account
        for (var account in objectData) {
            var tempAccount = objectData[account]
            if (tempAccount["email"] == loginEmail) {
                emailFound = true;
                localStorage.setItem("current_user", JSON.stringify(tempAccount));
            }
        }

        // Validate if the email match on the current data
        if (emailFound == false) {
            alert("Account does not exist!");
            console.log("Account does not exist!")
            $("#loginForm").trigger("reset");
            $('#txtLoginEmail').focus();
            event.preventDefault();

        } else {
            userData = localStorage.getItem("current_user");
            user = JSON.parse(userData);

            // Validate if password match the login email
            if (user["password"] != loginPassword) {
                alert("Incorrect email or password.");
                console.log("Incorrect email or password.")
                $("#loginForm").trigger("reset");
                $('#txtLoginEmail').focus();
                localStorage.removeItem("current_user");
                event.preventDefault();

            } else {
                // Set the global variable isLoggedOn to true and redirect to Account Page            
                localStorage.setItem("isLoggedOn", true);
            }
        }
    });
});
