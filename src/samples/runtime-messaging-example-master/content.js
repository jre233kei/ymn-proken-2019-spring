function sendMessage(message) {
  return new Promise((resolve, reject) => {
    try {
      chrome.runtime.sendMessage(message, resolve);
    } catch (err) {
      reject(err);
    }
  });
}

// Message to send
const message = { greeting: 'SET_BADGE_TEXT', text: '😀' };

// Click event handler
const handleClick = event => {
  // sendMessage returns a Promise,
  // so you can optionally use "then"
  // to handle the response
  sendMessage(message).then(message => {
    // Log the greeting sent back from background.js
    console.log('message from background.js:', message);
  });
};

// Create a simple button to send message
const button = document.createElement('button');
button.innerText = 'Set Badge Text';
button.onclick = handleClick;
document.body.append(button);
