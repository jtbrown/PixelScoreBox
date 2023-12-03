$(document).ready(function() {

    //Convert Team Names to caps and limit to 5 spaces
    //var home = $('#home h2').text();
    //var away = $('#away h2').text();
    //var atbat = $('span.atbat').text();
    //$('#home h2').text(home.substring(0,5).toUpperCase());
    //$('#away h2').text(away.substring(0,5).toUpperCase());
    //$('span.atbat').text(away.substring(0,5).toUpperCase());

    /*
    $('.editable').on('click', function() {
        var that = $(this);
        if (that.find('input').length > 0) {
            return;
        }
        var currentText = that.text();

        var $input = $('<input>').val(currentText)
        .css({
            'position': 'absolute',
            top: '0px',
            left: '0px',
            width: that.width(),
            height: that.height(),
            opacity: 0.9,
            padding: '10px'
        });

        $(this).append($input);

        // Handle outside click
        $(document).click(function(event) {
            if(!$(event.target).closest('.editable').length) {
                if ($input.val()) {
                    that.text($input.val());
                }
                that.find('input').remove();
            }
        });
    });
    */

});