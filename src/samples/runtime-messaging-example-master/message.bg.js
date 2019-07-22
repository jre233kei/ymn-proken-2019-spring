function listenForMessage(callback) {
  async function asyncCallback(message, sender) {
    // Make sure the callback returns a Promise
    return callback(message, sender);
  }

  function handleMessage(message, sender, sendResponse) {
    asyncCallback(message, sender)
      .then(result => ({
        success: true,
        ...result,
      }))
      .catch(reason => ({
        success: false,
        reason: reason.message || reason,
        stack: reason.stack || undefined,
      }))
      .then(msg => ({
        greeting: message.greeting,
        ...msg,
      }))
      .then(sendResponse);

    return true;
  }

  chrome.runtime.onMessage.addListener(handleMessage);
}
