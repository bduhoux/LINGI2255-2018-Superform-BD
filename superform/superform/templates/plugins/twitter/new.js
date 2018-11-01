$('input.checkbox').change(function () {
    nameC = $(this).attr('data-namechan');
    idC = $(this).attr('value');
    module = $(this).attr('data-module');
    if ($(this).is(':checked') && module == 'superform.plugins.Twitter') {
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
        var text_length = $('#' + channelName + '_descriptionpost').val().length;
        if ($('#' + channelName + '_linkurlpost').val() != '' && $('#' + channelName + '_linkurlpost').val() != null)
            text_length = text_length + 23;
        if (text_length >= 280) {
            $("label[for='" + channelName + "_" + $('#descriptionpost').attr('id') + "'] > a").remove();
            $("label[for='" + channelName + "_" + $('#descriptionpost').attr('id') + "']").append('<a href="#" data-toggle="popover" title="Content too long" data-content="Too many characters for one tweet"><i class="fas fa-exclamation-circle" style="color:orange"></i></a>');
            $("." + channelName + "_status_too_many_chars").remove();
            $("#" + channelName + "_card_body").append('<div class="' + channelName + '_status_too_many_chars"> Too many characters for one tweet! </div>');
            $("#card_body").append('<div class="' + channelName + '_status_too_many_chars">' + channelName + ': Too many characters for one tweet! </div>');
            $('[data-toggle="popover"]').popover();
        }
        else if (text_length == 0) {
            $("." + channelName + "_empty_description").remove();
            $("#" + channelName + "_card_body").append('<div class="' + channelName + '_empty_description"> Twitter publishings must contain a description! </div>');
            $("#card_body").append('<div class="' + channelName + '_empty_description">' + channelName + ': Twitter publishings must contain a description! </div>');
            $("#publish-button").prop('disabled', true);
            block_submit = true;
        }
        else if (text_length != 0) {
            block_submit = false;
            $("." + channelName + "_empty_description").remove();
            if (!invalid_input()) {
                $("#publish-button").prop('disabled', false);
            }
        } else {
            $("label[for='" + channelName + "_" + $('#descriptionpost').attr('id') + "'] > a").remove();
            $("." + channelName + "_status_too_many_chars").remove();
        }
        $('#' + channelName + '_textarea_feedback').html(text_length + '/279');
    }

    return charCounter;
}

function getTweetHtml(text, channelName, i, numberOfTweets) {
    var html = `<div class="form-group tweet-preview">
                    <label for="${channelName}_tweet_${i}">Tweet ${i}/${numberOfTweets}</label>
                    <input type="button" value="Remove" onclick="removePreviewTweet('${channelName}', ${i})"><br> 
                    <textarea class="form-control" rows="4" maxlength="280" id="${channelName}_tweet_${i}" name="${channelName}_tweet_${i}">${text}</textarea>
                </div>`;
    return html;
}

function addPreviewTweet(channelName) {
    var preview_container = $('#' + channelName + '_preview');
    var numberOfTweets = preview_container.children().length + 1;
    if (numberOfTweets == 0) {
        $('.tweet-preview').remove();
    }
    var i = 1;
    preview_container.children().each(function () {
        $(this).find('label').html(`Tweet ${i}/${numberOfTweets}`);
        i++;
    });
    var html = getTweetHtml('', channelName, numberOfTweets, numberOfTweets);
    preview_container.append(html);
}

function removePreviewTweet(channelName, tweetNumber) {
    var preview_container = $('#' + channelName + '_preview');
    var i = 1;
    var tweets = [];
    preview_container.children().each(function () {
        if (i != tweetNumber) {
            tweets.push($(this).find('textarea').text());
        }
        i++;
    });
    var numberOfTweets = preview_container.children().length - 1;
    $('.tweet-preview').remove();
    for (var i = 1; i <= numberOfTweets; i++) {
        var tweet = tweets[i - 1];
        console.log(tweet);
        var html = getTweetHtml(tweet, channelName, i, numberOfTweets);
        preview_container.append(html);
    }
}

function getTwitterPreviewUpdater(channelName) {
    function twitterUpdatePreview() {
        var text = $('#' + channelName + '_descriptionpost').val();
        var url = $('#' + channelName + '_linkurlpost').val();
        var tweets;
        if ($('#' + channelName + '_truncate').prop('checked')) {
            if (text.length + Math.min(url.length, 23) + 1 > 280) {
                tweets = [truncateTweet(text, url)];
            } else {
                tweets = [text + ' ' + url];
            }
        } else {
            tweets = splitTweet(text, url);
        }
        var preview_container = $('#' + channelName + '_preview');
        var numberOfTweets = tweets.length;
        $('.tweet-preview').remove();
        for (var i = 1; i <= numberOfTweets; i++) {
            var tweet = tweets[i - 1];
            console.log(tweet);
            var html = getTweetHtml(tweet, channelName, i, numberOfTweets);
            preview_container.append(html);
        }
    }

    return twitterUpdatePreview;
}

/**
 * Initializes the listeners for the Twitter channel given as argument
 * @param channelName: The name of the channel
 * @param channelID: The ID of the channel
 */
function initializeTwitterListeners(channelName, channelID) {
    var charCounter = getCharCounter(channelName);
    charCounter();
    $('#' + channelName + '_textarea_feedback').html('0/279');
    $('#' + channelName + '_descriptionpost').on('keyup', charCounter);
    $('#' + channelName + '_linkurlpost').on('keyup', charCounter);
    $('#descriptionpost').on('keyup', charCounter);
    $('#linkurlpost').on('keyup', charCounter);
    $('#li_' + channelName).on('click', charCounter);
    $('#chan_option_' + channelID).on('keyup', charCounter);

    var twitterUpdatePreview = getTwitterPreviewUpdater(channelName)
    twitterUpdatePreview()
    $('#' + channelName + '_descriptionpost').on("change", twitterUpdatePreview);
    $('#' + channelName + '_truncate').on("change", twitterUpdatePreview);
    $('#' + channelName + '_NotTruncate').on("change", twitterUpdatePreview);
    $('#' + channelName + '_linkurlpost').on("change", twitterUpdatePreview);
}


/**
 * Removes the listeners for the Twitter channel given as argument
 * @param channelName: The name of the channel
 * @param channelID: The ID of the channel
 */
function removeTwitterListeners(channelName, channelID) {
    $('#' + channelName + '_descriptionpost').off('keyup');
    $('#' + channelName + '_descriptionpost').off('change');
    $('#' + channelName + '_linkurlpost').off('keyup');
    $('#descriptionpost').off('keyup');
    $('#linkurlpost').off('keyup');
    $('#li_' + channelName).off('click');
    $('#chan_option_' + channelID).off('keyup');
    $("." + channelName + "_status_too_many_chars").remove();
    $("." + channelName + "_empty_description").remove();
}

function truncateTweet(text, url) {
    var tweet = '';
    var words = text.split(" ");
    console.log(words)
    var endingLength;
    if (url.length != 0) {
        endingLength = 6;
    } else {
        endingLength = 5;
    }
    for (var word of words) {
        var test_tweet = '';
        if (tweet == '') {
            test_tweet = tweet + word;
        } else {
            test_tweet = tweet + ' ' + word;
        }
        if (test_tweet.length + Math.min(url.length, 23) + endingLength <= 280) {
            tweet = test_tweet;
        } else {
            break;
        }
    }
    if (url.length != 0) {
        tweet = tweet + ' [\u2026] ' + url;
    } else {
        tweet = tweet + ' [\u2026]';
    }
    return tweet;
}

function splitTweet(text, url) {
    // the content of the current tweet
    var tweet_list = [];
    var tweet = '';
    var continuationLength = 8;
    // get the different words in the tweet
    var words = text.split(" ");
    for (var word of words) {
        // test to add the next word
        var test_tweet = '';
        if (tweet == '') {
            test_tweet = tweet + word;
        } else {
            test_tweet = tweet + ' ' + word;
        }
        // if we can add the next word we add it
        if (test_tweet.length + continuationLength + 2 <= 280) {
            tweet = test_tweet;
        }
        // if we can't publish
        else {
            tweet_list.push(tweet + '\u2026');
            tweet = word;
        }
    }
    if (tweet.length + 1 + Math.min(url.length, 23) <= 280) {
        tweet_list.push(tweet + ' ' + url);
    } else {
        tweet_list.push(tweet + '\u2026');
        tweet_list.push(url);
    }
    var numberOfTweets = tweet_list.length;
    if (numberOfTweets > 1) {
        for (var i = 1; i <= numberOfTweets; i++) {
            tweet_list[i - 1] = `[${i}/${numberOfTweets}] ` + tweet_list[i - 1];
        }
    }
    return tweet_list;

}
