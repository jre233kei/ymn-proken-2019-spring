/*chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
      if (request.greeting == "hello i come from content")
        sendResponse({farewell: "I came from the popup script!"});
    });
*/
var pageStr = "";

document.addEventListener('DOMContentLoaded', function () {
    // (Inside the click listener)
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.executeScript(tabs[0].id, { file: "js/content.js" }, function (data) {
            // Data is an array of values, in case it was executed in multiple tabs/frames
            //download(data[0], "download.html", "text/html");
            document.getElementById("title").textContent = data[0];
            //pageStr = data[0];
            //console.log(pageStr);

            //alert("Start messaging!");

            console.log(data[0])

            
            //send_str = "最悪な商品でした";

            

            axios.defaults.headers['Content-Type'] = 'text/plain;charset=utf-8';

            axios.post('https://g8kwped00b.execute-api.us-east-1.amazonaws.com/production', {
                text : encodeURIComponent(data[0])
            }).then(response => {
                //alert(response.data.body);
                console.log(response);
                //alert('結果: ' + response["data"]["body"]);
            }).catch(error => {
                alert(error);
            });;

        });
    });
});
