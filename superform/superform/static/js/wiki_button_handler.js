/*  Copyright 2004-2015 Patrick R. Michaud (pmichaud@pobox.com)
    This file is part of PmWiki; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published
    by the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.  See pmwiki.php for full details.

    This file provides Javascript functions to support WYSIWYG-style
    editing.  The concepts are borrowed from the editor used in Wikipedia,
    but the code has been rewritten from scratch to integrate better with
    PHP and PmWiki's codebase.
    
    Script maintained by Petko Yotov www.pmwiki.org/petko
*/

function previewFunction() {
    let tid = arguments[0].id;

    let text_area = document.getElementById(tid);

    let div_preview = document.createElement('div');
    div_preview.setAttribute("class", 'form-group');
    div_preview.setAttribute("id", "div_preview");

    let labelpreview = document.createElement('label');
    labelpreview.setAttribute("id","previewLabel");
    labelpreview.innerText = "Preview";
    labelpreview.setAttribute("for", "text_area_preview");

    //let text_area_preview = document.createElement('textarea');
    //text_area_preview.setAttribute("readonly","true");
    let text_area_preview = document.createElement('div');
    text_area_preview.setAttribute("id", "text_area_preview");
    //text_area_preview.setAttribute("class", "form-control");
    //text_area_preview.setAttribute("rows", "5");

    Element.prototype.appendAfter = function (element) {
        element.parentNode.insertBefore(this, element.nextSibling);
    }, false;

    div_preview.appendAfter(text_area.parentElement);
    div_preview.appendChild(labelpreview);
    div_preview.appendChild(text_area_preview);

    text_area.onkeyup = text_area.onkeypress = function(){document.getElementById('text_area_preview').innerHTML = interpreter(this.value);
    console.log(interpreter(this.value));};
}

function interpreter(str) {

    let res = str.replace(/\n/g,"<br>");
    res = replace_double_bold(res);
    res = replace_bold_italic(res);
    res = replace_double_italic(res);
    res = replace_bold(res);
    res = replace_italic(res);
    res = replace_link1(res);
    res = replace_link2(res);
    res = replace_big1(res);
    res = replace_big2(res);
    res = replace_small1(res);
    res = replace_small2(res);
    res = replace_sub1(res);
    res = replace_sub2(res);
    res = replace_exp1(res);
    res = replace_exp2(res);
    //res = replace_heading(res);
    //res = replace_center(res);

    return res;
}

function replace_double_bold(str){
    let old_string = str;
    let new_string = str;
    do{
        old_string = new_string;
        new_string = old_string.replace(/''''''/, "</strong><strong>" );
    }while(old_string!==new_string);
    return new_string;
}

function replace_bold_italic(str){
    let old_string = str;
    let new_string = str;
    let opened = false;
    do{
        old_string = new_string;
        if(opened) {
            new_string = old_string.replace(/'''''/, "</strong></em>");
            opened = false;
        }
        else{
            new_string = old_string.replace(/'''''/, "<strong><em>");
            opened = true;
        }
    }while(old_string!==new_string);
    return new_string;
}

function replace_double_italic(str){
    let old_string = str;
    let new_string = str;
    do{
        old_string = new_string;
        new_string = old_string.replace(/''''/, "</em><em>" );
    }while(old_string!==new_string);
    return new_string;
}

function replace_bold(str){
    let old_string = str;
    let new_string = str;
    let opened = false;
    do{
        old_string = new_string;
        if(opened) {
            new_string = old_string.replace(/'''/, "</strong>");
            opened = false;
        }
        else{
            new_string = old_string.replace(/'''/, "<strong>");
            opened = true;
        }
    }while(old_string!==new_string);
    return new_string;
}

function replace_italic(str){
    let old_string = str;
    let new_string = str;
    let opened = false;
    do{
        old_string = new_string;
        if(opened) {
            new_string = old_string.replace(/''/, "</em>");
            opened = false;
        }
        else{
            new_string = old_string.replace(/''/, "<em>");
            opened = true;
        }
    }while(old_string!==new_string);
    return new_string;
}

function replace_link1(str){
    let href = get_href(str);
    let str2 = "<a class=\"urllink\" href=\""+href+"\">";
    return str.replace(/\[\[/g,str2);
}

function replace_link2(str){
    let str2 = "</a>";
    return str.replace(/]]/g,str2);
}

function get_href(str){
    var count1 = (str.match(/\[\[/g) || []).length; //occurence de [[
    var count2 = (str.match(/]]/g) || []).length; //occurence de ]]

    if(count1 >= 1){
        var pos1 = str.indexOf("[[")+2;
        var pos2 = str.indexOf("]]");
        var str2 = str.substring(pos1, pos2);
        return str2;
    }
}

function replace_big1(str) {
    let str2 = "<big>";
    return str.replace(/'\+/g,str2);
}

function replace_big2(str) {
    let str2 = "</big>";
    return str.replace(/\+'/g,str2);
}

function replace_small1(str) {
    let str2 = "<small>";
    return str.replace(/'-/g,str2);
}

function replace_small2(str) {
    let str2 = "</small>";
    return str.replace(/-'/g,str2);
}

function replace_exp1(str) {
    let str2 = "<sup>";
    return str.replace(/'\^/g,str2);
}

function replace_exp2(str) {
    let str2 = "</sup>";
    return str.replace(/\^'/g,str2);
}

function replace_sub1(str) {
    let str2 = "<sub>";
    return str.replace(/'_/g,str2);
}

function replace_sub2(str) {
    let str2 = "</sub>";
    return str.replace(/_'/g,str2);
}

function replace_heading(str) {
    str = str.replace(/!!/,"<h1>");
    var i = str.charAt("<h1>");
    do {
        i++;
    }while (str.substring(i,i+2) !== "\n")
    str = str.substring(0,i) + "</h1>" + str.substring(i+2,str.length);
}

function insButton(mopen, mclose, mtext, mlabel, mkey) {
    console.log("insButton");
    if (mkey > '') { mkey = 'accesskey="' + mkey + '" ' }
    document.write("<a tabindex='-1' "+ mkey + "onclick=\"insMarkup('"
        + mopen + "','"
        + mclose + "','"
        + mtext + "');\">"
        + mlabel + "</a>");
}

function insMarkup() {
    var func = false, tid='wiki_descriptionpost', mopen = '', mclose = '', mtext = '';
    if(typeof arguments[0] == 'function') {
        var func = arguments[0];
        if(arguments.length > 1) tid = arguments[1];
        mtext = func('');
    }
    else if (arguments.length >= 3) {
        var mopen = arguments[0], mclose = arguments[1], mtext = arguments[2];
        if(arguments.length > 3) {
            tid = arguments[3];
            tid = tid.id;
        }
    }

    var tarea = document.getElementById(tid);

    if (tarea.setSelectionRange > '') {
        var p0 = tarea.selectionStart;
        var p1 = tarea.selectionEnd;
        var top = tarea.scrollTop;
        var str = mtext;
        var cur0 = p0 + mopen.length;
        var cur1 = p0 + mopen.length + str.length;
        while (p1 > p0 && tarea.value.substring(p1-1, p1) == ' ') p1--;
        if (p1 > p0) {
            str = tarea.value.substring(p0, p1);
            if(func) str = func(str);
            cur0 = p0 + mopen.length + str.length + mclose.length;
            cur1 = cur0;
        }
        tarea.value = tarea.value.substring(0,p0)
            + mopen + str + mclose
            + tarea.value.substring(p1);
        tarea.focus();
        tarea.selectionStart = cur0;
        tarea.selectionEnd = cur1;
        tarea.scrollTop = top;
    } else if (document.selection) {
        var str = document.selection.createRange().text;
        tarea.focus();
        let range = document.selection.createRange();
        if (str == '') {
            range.text = mopen + mtext + mclose;
            range.moveStart('character', -mclose.length - mtext.length );
            range.moveEnd('character', -mclose.length );
        } else {
            if (str.charAt(str.length - 1) == " ") {
                mclose = mclose + " ";
                str = str.substr(0, str.length - 1);
                if(func) str = func(str);
            }
            range.text = mopen + str + mclose;
        }
        range.select();
    } else { tarea.value += mopen + mtext + mclose; }
    return;
}


