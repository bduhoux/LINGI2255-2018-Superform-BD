function getTweetHtml(text, i, numberOfTweets) {
    var html = `<div class="form-group tweet-preview">
                    <label for="tweet_${i}">Tweet ${i}/${numberOfTweets}</label>
                    <input type="button" value="Remove" onclick="removePreviewTweet(${i})"><br> 
                    <textarea class="form-control" rows="4" maxlength="280" id="tweet_${i}" name="tweet_${i}">${text}</textarea>
                </div>`;
    return html;
}

function addPreviewTweet() {
    var preview_container = $('#preview');
    var numberOfTweets = preview_container.children().length + 1;
    if (numberOfTweets == 0) {
        $('.tweet-preview').remove();
    }
    var i = 1;
    preview_container.children().each(function () {
        $(this).find('label').html(`Tweet ${i}/${numberOfTweets}`);
        i++;
    });
    var html = getTweetHtml('', numberOfTweets, numberOfTweets);
    preview_container.append(html);
}

function removePreviewTweet(tweetNumber) {
    var preview_container = $('#preview');
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
        var html = getTweetHtml(tweet, i, numberOfTweets);
        preview_container.append(html);
    }
}