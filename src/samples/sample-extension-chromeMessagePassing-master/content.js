
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.instructions === "giveMeFirstImgPlease") {
    var firstImgTag = 'http:' + $('body').find('img').attr('src').replace(/http:|https:/, '');
    var msgBackToExt = {fromTab: "imgTagAsRequested", imgTagSrc: firstImgTag};
    sendResponse(msgBackToExt);
  }
});
