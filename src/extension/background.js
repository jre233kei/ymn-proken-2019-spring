var textContents = '';
chrome.runtime.onMessage.addListener(
  function (request, sender, sendResponse){
    textContents = request.value;
  }
);

var port = chrome.runtime.connectNative("sample_app");
 
/*
Listen for messages from the app.
*/
port.onMessage.addListener((response) => {
  console.log("Received: " + response);
});

/*
On a click on the browser action, send the app a message.
*/
chrome.browserAction.onClicked.addListener(() => {
  console.log("Sending:  ping");
  port.postMessage("ping");
});
