
//Transparent Navigation


$(function () {

    //show/hide nav on page load
    showHideNav();

    $(window).scroll(function () {

        //show/hide nav on windows Scroll
        showHideNav();
    });

    function showHideNav() {
        if ($(window).scrollTop() > 80) {

            $("nav").removeClass("transparent-nav");
            // show white nav
            $("nav").addClass("white-nav-top");
            // show dark logo
            $(".navbar-brand img").attr("src", "images/logo/Campus.png");

            //show back to top button
           // $("#back-to-top").fadeIn();

        } else {

            $("nav").removeClass("white-nav-top");

            $("nav").addClass("transparent-nav");
            // hide white nav

            //normal logo

            $(".navbar-brand img").attr("src", "images/logo/Campus.png");

            //hide back to top button
           // $("#back-to-top").fadeOut();
        }
    }
});
