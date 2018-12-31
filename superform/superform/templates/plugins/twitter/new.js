// Initialize listeners
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
 * Returns a function that displays warnings when the number of chars is greater than 280.
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
            $("#" + channelName + "_card_body").append('<span class="' + channelName + '_status_too_many_chars" id="status_too_many_chars"> Too many characters for one tweet! </span>');
            $("#card_body").append('<span class="' + channelName + '_status_too_many_chars" >' + channelName + ': Too many characters for one tweet! </span>');
            $('[data-toggle="popover"]').popover();
        } else {
            $("label[for='" + channelName + "_" + $('#descriptionpost').attr('id') + "'] > a").remove();
            $("." + channelName + "_status_too_many_chars").remove();
        }
    }

    return charCounter;
}

/**
 * Counts the number of chars in a tweet preview and displays it.
 * @param channelName: The name of the channel
 */
function getTweetCharCounter(channelName) {
    function tweetCharCounter(event) {
        var tweetTextarea = $(this);
        var tweetContainer = tweetTextarea.parent();
        var text = tweetTextarea.val();
        var text_length = text.length;
        var re_url = /\(?(?:(http|https|ftp):\/\/)?(?:((?:[^\W\s]|\.|-|[:]{1})+)@{1})?((?:www.)?(?:[^\W\s]|\.|-)+[\.][^\W\s]{2,4}|localhost(?=\/)|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::(\d*))?([\/]?[^\s\?]*[\/]{1})*(?:\/?([^\s\n\?\[\]\{\}\#]*(?:(?=\.)){1}|[^\s\n\?\[\]\{\}\.\#]*)?([\.]{1}[^\s\?\#]*)?)?(?:\?{1}([^\s\n\#\[\]]*))?([\#][^\s\n]*)?\)?/gi;
        var urls = text.match(re_url);
        if (urls != null) {
            for (url of urls) {
                text_length -= url.length;
                text_length += 23;
            }
        }
        var re_special_chars = /\u2026/gi;
        var special_chars = text.match(re_special_chars);
        if (special_chars != null) {
            text_length += special_chars.length;
        }
        if (text_length == 0) {
            $("." + channelName + "_empty_description").remove();
            $("#" + channelName + "_card_body").append('<div class="' + channelName + '_empty_description"> Tweets cannot be empty! </div>');
            $("#card_body").append('<div class="' + channelName + '_empty_description">' + channelName + ': Tweets cannot be empty! </div>');
            $("#publish-button").prop('disabled', true);
            block_submit = true;
        }
        else if (text_length > 280) {
            $("." + channelName + "_tweet_too_many_chars").remove();
            $("#" + channelName + "_card_body").append('<div class="' + channelName + '_tweet_too_many_chars"> Tweets cannot contain more than 280 characters! </div>');
            $("#card_body").append('<div class="' + channelName + '_tweet_too_many_chars"> ' + channelName + ': Tweets cannot contain more than 280 characters! </div>');
            $("#publish-button").prop('disabled', true);
            block_submit = true;
        } else {
            block_submit = false;
            $("." + channelName + "_empty_description").remove();
            $("." + channelName + "_tweet_too_many_chars").remove();
            if (!invalid_input()) {
                $("#publish-button").prop('disabled', false);
            }
        }
        tweetContainer.find('.tweet-char-counter').html('(' + text_length + ' out of 280 characters)');
    }

    return tweetCharCounter;
}

/**
 * Returns a formatted tweet preview.
 * @param text: the text to put in the tweet preview
 * @param channelName: the name of this Twitter channel
 * @param i: the number of this tweet
 * @param numberOfTweets: the total number of tweets
 * @returns a {string} containing the tweet preview formatted in html
 */
function getTweetHtml(text, channelName, i, numberOfTweets) {
    var html = `<div class="form-group tweet-preview">
                    <label for="${channelName}_tweet_${i}"> <span class="${channelName}-tweet-number"> Tweet ${i}/${numberOfTweets} </span> <span id="NumberCharacters_${i}" class="tweet-char-counter" style="font-style: italic"></span></label>
                    <input type="button" value="Remove" onclick="removePreviewTweet('${channelName}', ${i})"><br> 
                    <textarea class="form-control" rows="4" id="${channelName}_tweet_${i}" name="${channelName}_tweet_${i}">${text}</textarea>
                </div>`;
    return html;
}

/**
 * Adds a new tweet preview in the preview container and updates the numbering of the tweets accordingly.
 * @param channelName: the name of this Twitter channel
 */
function addPreviewTweet(channelName) {
    var tweetCharCounter = getTweetCharCounter(channelName);
    var preview_container = $('#' + channelName + '_preview');
    $('#' + channelName + '_no_preview').remove();
    var numberOfTweets = preview_container.children().length + 1;
    var i = 1;
    preview_container.children().each(function () {
        $(this).find('.' + channelName + '-tweet-number').html(`Tweet ${i}/${numberOfTweets}`);
        i++;
    });
    var html = getTweetHtml('', channelName, numberOfTweets, numberOfTweets);
    preview_container.append(html);
    var tweetContainer = $('#' + channelName + '_tweet_' + numberOfTweets);
    tweetContainer.on('keyup', tweetCharCounter);
    tweetContainer.trigger('keyup', 'update char count');
}

/**
 * Removes the tweet preview given as argument from the preview container and updates the numbering of the tweets accordingly.
 * @param channelName: the name of this Twitter channel
 * @param tweetNumber: the number of the tweet preview to delete
 */
function removePreviewTweet(channelName, tweetNumber) {
    var preview_container = $('#' + channelName + '_preview');
    var i = 1;
    var tweets = [];
    preview_container.children().each(function () {
        if (i != tweetNumber) {
            tweets.push($(this).find('textarea').val());
            console.log($(this).find('textarea').val());
        }
        i++;
    });
    addTweetsToHtml(tweets, channelName);
}

/**
 * Returns a function that updates the preview of the tweets according to the parameters selected by the user
 * of the app.
 * @param channelName: the name of this Twitter channel
 * @returns a function {twitterUpdatePreview}
 */
function getTwitterPreviewUpdater(channelName) {
    function twitterUpdatePreview() {
        var text = $('#' + channelName + '_descriptionpost').val();
        var url = $('#' + channelName + '_linkurlpost').val();
        var tweets;
        if ($('#' + channelName + '_truncate').prop('checked')) {
            if (text.length + 23 + 1 > 280) {
                tweets = [truncateTweet(text, url)];
            } else {
                tweets = [text + ' ' + url];
            }
        } else {
            tweets = splitTweet(text, url);
        }
        addTweetsToHtml(tweets, channelName);
    }

    return twitterUpdatePreview;
}

/**
 * Adds the tweets given as argument to the preview container.
 * @param tweets: a list of {strings} containing the text of the tweets
 * @param channelName: the name of this Twitter channel
 */
function addTweetsToHtml(tweets, channelName) {
    var tweetCharCounter = getTweetCharCounter(channelName);
    var preview_container = $('#' + channelName + '_preview');
    $('#' + channelName + '_no_preview').remove();
    var numberOfTweets = tweets.length;
    $('.tweet-preview').remove();
    for (var i = 1; i <= numberOfTweets; i++) {
        var tweet = tweets[i - 1];
        var html = getTweetHtml(tweet, channelName, i, numberOfTweets);
        preview_container.append(html);
        var tweetContainer = $('#' + channelName + '_tweet_' + i);
        tweetContainer.on('keyup', tweetCharCounter);
        tweetContainer.trigger('keyup', 'update char count');
    }
    if (numberOfTweets == 0) {
        var html = `<div class="form-group tweet-preview" id="${channelName}_no_preview"> No preview yet. </div>`;
        $("." + channelName + "_empty_description").remove();
        $("." + channelName + "_tweet_too_many_chars").remove();
        preview_container.append(html);
    }
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
    $('#descriptionpost').one("change", twitterUpdatePreview);
    $('#linkurlpost').one("change", twitterUpdatePreview);
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

/**
 * Truncates the text given as argument to make it fit into a single tweet (if necessary). The url is never truncated
 * but will be put a the end of the tweet.
 * @param text: the content of the tweet (non truncated)
 * @param url: the url to add to the tweet (if not null)
 * @returns a {string} containing the text and url of the tweet
 */
function truncateTweet(text, url) {
    var tweet = '';
    var words = text.split(" ");
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
        if (test_tweet.length + 23 + endingLength <= 280) {
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

/**
 * Splits the text given as argument into blocks of less than 280 characters.
 * @param text: the content of the tweet(s)
 * @param url: the url to add to the tweet (if not null)
 * @returns an {Array} containing the tweet(s) created
 */
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
        if (tweet === '') {
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
    if (tweet.length + 1 + 23 <= 280) {
        if (url.length > 0) {
            tweet_list.push(tweet + ' ' + url);
        } else {
            tweet_list.push(tweet);
        }
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
