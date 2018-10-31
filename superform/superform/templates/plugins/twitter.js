$('input.checkbox').change(function () {
    nameC = $(this).attr('data-namechan');
    idC = $(this).attr('value');
    module = $(this).attr('data-module');
    if ($(this).is(':checked')) {
        initializeTwitterListeners(nameC, idC);
    } else {
        //If the channel is not selected
        removeTwitterListeners(nameC, idC);
    }
});
/**
 * Returns a function that displays the number of chars in the description field of the publication. The
 * function also displays warnings when the number of chars is greater than 279.
 * @param channelName: The name of the channel
 */
function getCharCounter(channelName) {
    function charCounter(event) {
        var text_length = $('#'+channelName+'_descriptionpost').val().length;
        if ($('#'+channelName+'_linkurlpost').val() != '' && $('#'+channelName+'_linkurlpost').val() != null)
            text_length = text_length + 23;
        if (text_length >= 280) {
            $("label[for='" + channelName + "_" + $('#descriptionpost').attr('id') + "'] > a").remove();
            $("label[for='" + channelName + "_" + $('#descriptionpost').attr('id') + "']").append('<a href="#" data-toggle="popover" title="Content too long" data-content="Too many characters for one tweet"><i class="fas fa-exclamation-circle" style="color:orange"></i></a>');
            $("."+channelName+"_status_too_many_chars").remove();
            $("#"+channelName+"_card_body").append('<div class="'+channelName+'_status_too_many_chars"> Too many characters for one tweet! </div>');
            $("#card_body").append('<div class="'+channelName+'_status_too_many_chars">'+channelName+': Too many characters for one tweet! </div>');
            $('[data-toggle="popover"]').popover();
        } else {
            $("label[for='" + channelName + "_" + $('#descriptionpost').attr('id') + "'] > a").remove();
            $("."+channelName+"_status_too_many_chars").remove();
        }
        $('#'+channelName+'_textarea_feedback').html(text_length + '/279');
    }
    return charCounter;
}


/**
 * Initializes the listeners for the Twitter channel given as argument
 * @param channelName: The name of the channel
 * @param channelID: The ID of the channel
 */
function initializeTwitterListeners(channelName, channelID) {
    getCharCounter(channelName)(null);
    $('#'+channelName+'_textarea_feedback').html('0/279');
    $('#'+channelName+'_descriptionpost').on('keyup', getCharCounter(channelName));
    $('#'+channelName+'_linkurlpost').on('keyup', getCharCounter(channelName));
    $('#descriptionpost').on('keyup', getCharCounter(channelName));
    $('#linkurlpost').on('keyup', getCharCounter(channelName));
    $('#li_'+channelName).on('click', getCharCounter(channelName));
    $('#chan_option_'+channelID).on('keyup', getCharCounter(channelName));
}


/**
 * Removes the listeners for the Twitter channel given as argument
 * @param channelName: The name of the channel
 * @param channelID: The ID of the channel
 */
function removeTwitterListeners(channelName, channelID) {
    $('#'+channelName+'_descriptionpost').off('keyup');
    $('#'+channelName+'_linkurlpost').off('keyup');
    $('#descriptionpost').off('keyup');
    $('#linkurlpost').off('keyup');
    $('#li_'+channelName).off('click');
    $('#chan_option_'+channelID).off('keyup');
    $("."+channelName+"_status_too_many_chars").remove();
}