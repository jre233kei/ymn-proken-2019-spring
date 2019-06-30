var textContents = chrome.extension.getBackgroundPage().textContents;
var div = document.getElementById('textView');
div.textContent = textContents;