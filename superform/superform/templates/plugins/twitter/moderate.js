// Set handler functions
var tweets = $('.tweet-preview');
tweets.each(function () {
    var tweetContainer = $(this).find('textarea');
    tweetContainer.on('keyup', tweetCharCounter);
    tweetContainer.trigger('keyup', 'update char count');
});

/**
 * Counts the number of chars in a tweet preview and displays it.
 * @param event: an event
 */
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
    tweetContainer.find('.tweet-char-counter').html('(' + text_length + ' out of 280 characters)');
}

/**
 * Returns a formatted tweet preview.
 * @param text: the text to put in the tweet preview
 * @param i: the number of this tweet
 * @param numberOfTweets: the total number of tweets
 * @returns a {string} containing the tweet preview formatted in html
 */
function getTweetHtml(text, i, numberOfTweets) {
    var html = `<div class="form-group tweet-preview">
                    <label for="tweet_${i}"> <span class="tweet-number"> Tweet ${i}/${numberOfTweets} </span> <span class="tweet-char-counter" style="font-style: italic"></span></label>
                    <input type="button" value="Remove" onclick="removePreviewTweet(${i})"><br> 
                    <textarea class="form-control" rows="4" id="tweet_${i}" name="tweet_${i}">${text}</textarea>
                </div>`;
    return html;
}

/**
 * Adds a new tweet preview in the preview container.
 */
function addPreviewTweet() {
    var preview_container = $('#preview');
    $('#no_preview').remove();
    var numberOfTweets = preview_container.children().length + 1;
    var i = 1;
    preview_container.children().each(function () {
        $(this).find('.tweet-number').html(`Tweet ${i}/${numberOfTweets}`);
        i++;
    });
    var html = getTweetHtml('', numberOfTweets, numberOfTweets);
    preview_container.append(html);
    var tweetContainer = $('#tweet_' + numberOfTweets);
    tweetContainer.on('keyup', tweetCharCounter);
    tweetContainer.trigger('keyup', 'update char count');
}

/**
 * Removes the tweet preview given as argument from the preview container and updates the numbering of the tweets accordingly.
 * @param tweetNumber: the number of the tweet preview to delete
 */
function removePreviewTweet(tweetNumber) {
    var preview_container = $('#preview');
    var i = 1;
    var tweets = [];
    preview_container.children().each(function () {
        if (i !== tweetNumber) {
            tweets.push($(this).find('textarea').val());
            console.log($(this).find('textarea').val());
        }
        i++;
    });
    addTweetsToHtml(tweets);
}

/**
 * Adds the tweets given as argument to the preview container.
 * @param tweets: a list of {strings} containing the text of the tweets
 */
function addTweetsToHtml(tweets) {
    var preview_container = $('#preview');
    $('#no_preview').remove();
    var numberOfTweets = tweets.length;
    $('.tweet-preview').remove();
    for (var i = 1; i <= numberOfTweets; i++) {
        var tweet = tweets[i - 1];
        var html = getTweetHtml(tweet, i, numberOfTweets);
        preview_container.append(html);
        var tweetContainer = $('#tweet_' + i);
        tweetContainer.on('keyup', tweetCharCounter);
        tweetContainer.trigger('keyup', 'update char count');
    }
    if (numberOfTweets === 0) {
        var html = '<div class="form-group tweet-preview" id="no_preview"> No preview yet. </div>';
        preview_container.append(html);
    }
}