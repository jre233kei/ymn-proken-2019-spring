console.log('hey');
$(document).ready(function() {
  $('#btn').on('click', function() {
    var messageToTab = {instructions: "giveMeFirstImgPlease"};
    chrome.tabs.getSelected(null, function(tab) {
      chrome.tabs.sendMessage(tab.id, messageToTab, function(res) {
        $('img').remove();
        $('#infoFromTabDOM').append('<img src="'+res.imgTagSrc+'"/>');
      });
    });
  });
});
