document.querySelector('.like-button').addEventListener('click', (e) => {
    e.currentTarget.classList.toggle('liked');
    });

    $('#imgDetailsGalleryCol1Image2').click(function(){
        $(this).children('img').fadeOut(0);
        $('.product-gallery-column2').children('img').fadeOut(0);
        var x = $(this).children('img').attr('src');
        var y = $('.product-gallery-column2').children('img').attr('src');
        $(this).children('img').attr('src',y);
        $('.product-gallery-column2').children('img').attr('src',x);
        $('.product-gallery-column2').children('img').fadeIn(1500);
        $(this).children('img').fadeIn(1500);
        
        
    });

    $('#imgDetailsGalleryCol1Image1').click(function(){
        $(this).children('img').fadeOut(0);
        $('.product-gallery-column2').children('img').fadeOut(0);
        var x = $(this).children('img').attr('src');
        var y = $('.product-gallery-column2').children('img').attr('src');
        $(this).children('img').attr('src',y);
        $('.product-gallery-column2').children('img').attr('src',x);
        $('.product-gallery-column2').children('img').fadeIn(1500);
        $(this).children('img').fadeIn(1500);
    });

    $('#imgDetailsGalleryCol1Image3').click(function(){
        $(this).children('img').fadeOut(0);
        $('.product-gallery-column2').children('img').fadeOut(0);
        var x = $(this).children('img').attr('src');
        var y = $('.product-gallery-column2').children('img').attr('src');
        $(this).children('img').attr('src',y);
        $('.product-gallery-column2').children('img').attr('src',x);
        $('.product-gallery-column2').children('img').fadeIn(1500);
        $(this).children('img').fadeIn(1500);
    });
