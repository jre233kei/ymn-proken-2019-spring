/*chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
      if (request.greeting == "hello i come from content")
        sendResponse({farewell: "I came from the popup script!"});
    });
*/


document.addEventListener('DOMContentLoaded', function () {
    // (Inside the click listener)
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.executeScript(tabs[0].id, { file: "js/content.js" }, function (data) {
            // Data is an array of values, in case it was executed in multiple tabs/frames
            //download(data[0], "download.html", "text/html");
            document.getElementById("title").textContent = data[0];
        });
    });
});