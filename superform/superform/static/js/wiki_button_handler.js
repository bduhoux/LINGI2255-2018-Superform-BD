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
    tid = arguments[0].id;
    console.log(tid);
    tarea = document.getElementById(tid);
    console.log(tarea);
    var divpreview = document.createElement('div');
    console.log(divpreview);
    divpreview.setAttribute("id", "previewWiki");
    Element.prototype.appendAfter = function (element) {
        element.parentNode.insertBefore(this, element.nextSibling);
    }, false;
    divpreview.appendAfter(tarea.parentElement);
    tarea.onkeyup = tarea.onkeypress = function(){document.getElementById('previewWiki').innerHTML = this.value;};
}

function insButton(mopen, mclose, mtext, mlabel, mkey) {
  console.log("insButton");
  if (mkey > '') { mkey = 'accesskey="' + mkey + '" ' }
  document.write("<a tabindex='-1' " + mkey + "onclick=\"insMarkup('"
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
        console.log(tid);
        tid = tid.id;
        console.log(tid);
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
    range = document.selection.createRange();
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


