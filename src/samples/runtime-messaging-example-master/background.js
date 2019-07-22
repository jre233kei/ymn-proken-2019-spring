// Set up an event listener for runtime messages
listenForMessage((message, sender) => {
  switch (message.greeting) {
    case 'SET_BADGE_TEXT':
      console.log('message from content.js:', message);
      chrome.browserAction.setBadgeText({ text: message.text });
      return { greeting: 'BADGE_TEXT_WAS_SET' };
    default: // do nothing
  }
});
