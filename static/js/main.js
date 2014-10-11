/**
 * Created by Liyuwiki.com on 2014-6.
 */

(function($){

    $.fn.simplyCountable = function(options){

        options = $.extend({
            counter:            '#counter',
            countType:          'characters',
            maxCount:           140,
            strictMax:          false,
            countDirection:     'down',
            safeClass:          'safe',
            overClass:          'over',
            thousandSeparator:  ',',
            onOverCount:        function(){},
            onSafeCount:        function(){},
            onMaxCount:         function(){}
        }, options);

        var navKeys = [33,34,35,36,37,38,39,40];

        return $(this).each(function(){

            var countable = $(this);
            var counter = $(options.counter);
            if (!counter.length) { return false; }

            var countCheck = function(){

                var count;
                var revCount;

                var reverseCount = function(ct){
                    return ct - (ct*2) + options.maxCount;
                }

                var countInt = function(){
                    return (options.countDirection === 'up') ? revCount : count;
                }

                var numberFormat = function(ct){
                    var prefix = '';
                    if (options.thousandSeparator){
                        ct = ct.toString();
                        // Handle large negative numbers
                        if (ct.match(/^-/)) {
                            ct = ct.substr(1);
                            prefix = '-';
                        }
                        for (var i = ct.length-3; i > 0; i -= 3){
                            ct = ct.substr(0,i) + options.thousandSeparator + ct.substr(i);
                        }
                    }
                    return prefix + ct;
                }

                var changeCountableValue = function(val){
                    countable.val(val).trigger('change');
                }

                /* Calculates count for either words or characters */
                if (options.countType === 'words'){
                    count = options.maxCount - $.trim(countable.val()).split(/\s+/).length;
                    if (countable.val() === ''){ count += 1; }
                }
                else { count = options.maxCount - countable.val().length; }
                revCount = reverseCount(count);

                /* If strictMax set restrict further characters */
                if (options.strictMax && count <= 0){
                    var content = countable.val();
                    if (count < 0) {
                        options.onMaxCount(countInt(), countable, counter);
                    }
                    if (options.countType === 'words'){
                        var allowedText = content.match( new RegExp('\\s?(\\S+\\s+){'+ options.maxCount +'}') );
                        if (allowedText) {
                            changeCountableValue(allowedText[0]);
                        }
                    }
                    else { changeCountableValue(content.substring(0, options.maxCount)); }
                    count = 0, revCount = options.maxCount;
                }

                counter.text(numberFormat(countInt()));

                /* Set CSS class rules and API callbacks */
                if (!counter.hasClass(options.safeClass) && !counter.hasClass(options.overClass)){
                    if (count < 0){ counter.addClass(options.overClass); }
                    else { counter.addClass(options.safeClass); }
                }
                else if (count < 0 && counter.hasClass(options.safeClass)){
                    counter.removeClass(options.safeClass).addClass(options.overClass);
                    options.onOverCount(countInt(), countable, counter);
                }
                else if (count >= 0 && counter.hasClass(options.overClass)){
                    counter.removeClass(options.overClass).addClass(options.safeClass);
                    options.onSafeCount(countInt(), countable, counter);
                }

            };

            countCheck();

            countable.on('keyup blur paste', function(e) {
                switch(e.type) {
                    case 'keyup':
                        // Skip navigational key presses
                        if ($.inArray(e.which, navKeys) < 0) { countCheck(); }
                        break;
                    case 'paste':
                        // Wait a few miliseconds if a paste event
                        setTimeout(countCheck, (e.type === 'paste' ? 5 : 0));
                        break;
                    default:
                        countCheck();
                        break;
                }
            });

        });

    };

})(jQuery);


$(document).ready(function(){
    $("#id_term").focusin(function(){
        $("#id_term_tips").fadeIn(1000);
        $('#id_term').simplyCountable({
                counter: '#id_term_counter',
                countType: 'Character',
                maxCount: 20,
                countDirection: 'down'
            });
    });

    $("#id_term").focusout(function(){
        $("#id_term_tips").fadeOut(1000);
    });

    $("#id_definition").focusin(function(){
        $("#id_definition_tips").fadeIn(1000);
        $('#id_definition').simplyCountable({
            counter: '#id_definition_counter',
            countType: 'Character',
            maxCount: 200,
            countDirection: 'down'
        });
        $('#id_definition').simplyCountable({
            counter: '#id_definition_counter2',
            countType: 'Character',
            maxCount: 200,
            countDirection: 'up'
        });
    });
    $("#id_definition").focusout(function(){
        $("#id_definition_tips").fadeOut(1000);
    });

    $("#id_author").focusin(function(){
        $("#id_author_tips").fadeIn(1000);
        $('#id_author').simplyCountable({
            counter: '#id_author_counter',
            countType: 'Character',
            maxCount: 65,
            countDirection: 'down'
        });
    });
    $("#id_author").focusout(function(){
        $("#id_author_tips").fadeOut(1000);
    });

    $("#id_homepage").focusin(function(){
        $("#id_homepage_tips").fadeIn(1000);
        $('#id_homepage').simplyCountable({
            counter: '#id_homepage_counter',
            countType: 'Character',
            maxCount: 200,
            countDirection: 'down'
        });
    });
    $("#id_homepage").focusout(function(){
        $("#id_homepage_tips").fadeOut(1000);
    });

    $("#id_author_email").focusin(function(){
        $("#id_author_email_tips").fadeIn(1000);
        $('#id_author_email').simplyCountable({
            counter: '#id_author_email_counter',
            countType: 'Character',
            maxCount: 60,
            countDirection: 'down'
        });
    });
    $("#id_author_email").focusout(function(){
        $("#id_author_email_tips").fadeOut(1000);
    });

});

