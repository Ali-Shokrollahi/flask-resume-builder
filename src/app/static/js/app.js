$(document).ready(function () {
    var titel_counter = 0;
    var des_counter = 0;
    var Titletxt = "رزومه باز";
    var Destxt = "رزومه آنلاین خود را در 10 دقیقه بسازید";
    var title = $(".header__title");
    var des = $(".header__description");

    function typeHeaderTitle() {
        var text = title.html();
        title.html(text + Titletxt[titel_counter]);
        titel_counter++;
        var time = setTimeout(typeHeaderTitle, 100);
        if (titel_counter >= Titletxt.length) {
            clearTimeout(time);
        }
    }

    function typeHeaderDes() {
        var text = des.html();
        des.html(text + Destxt[des_counter]);
        des_counter++;
        var time = setTimeout(typeHeaderDes, 80);
        if (des_counter >= Destxt.length) {
            clearTimeout(time);
        }
    }


    typeHeaderTitle();
    typeHeaderDes();


    var icon = $(".menu__icon");
    var menu = $(".nav__list");

    icon.on("click", function () {
        if (icon.hasClass("fa-bars")) {
            menu.css("left", 0);
            icon.attr("class", "fa fa-times menu__icon");
        } else {
            menu.css("left", "-250px");
            icon.attr("class", "fa fa-bars menu__icon");
        }
    });

    var show_pass = $("#show_pass");

    show_pass.on("click", function () {
        var input = $(this).parent().find("input");
        if (input.attr("type") === "password") {
            this.innerHTML = '<i class="fa fa-eye c-blue"></i>';
            input.attr("type", "text");
        } else if (input.attr("type") === "text") {
            this.innerHTML = '<i class="fa fa-eye-slash c-blue"></i>';
            input.attr("type", "password");
        }
    });

    setTimeout(function () {
        $('#flash-messages').fadeOut('slow');
    }, 4000);

    $('.main-carousel').flickity({
        // options
        cellAlign: 'right',
        contain: true,
        prevNextButtons: false,
        pageDots: false,
        groupCells: false,
        autoPlay: true


    });
})
;



