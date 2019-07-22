console.log("I'm running");
/*chrome.runtime.sendMessage({greeting: "hello i come from content"}, function(response) {
    console.log(response.farewell);
  });*/
  DOMtoString(document); // This will be the last executed statement

  function DOMtoString(document_root) {
      console.log(document_root.body.innerText);
      return document_root.body.innerText;
  }