$(function() {
  var text = '';
  $("p").each(function() {
    text +=  $(this).text();
  });
  alert(text);
  chrome.runtime.sendMessage({
    value: document.getElementsByTagName('body')[0].outerText
  });
});