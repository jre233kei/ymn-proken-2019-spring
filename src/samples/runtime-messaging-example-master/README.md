# How to set an extension icon badge from a content script

Chrome Extension browser action badges can only be modified from the Extension background page, so we need a way to communicate **from** the content script **to** the background page. We can use Chrome Runtime Messaging to accomplish this.

The Chrome Runtime Messaging API can [be confusing to use](https://stackoverflow.com/questions/20077487/chrome-extension-message-passing-response-not-sent#comment64245056_20077854), so we'll make it easier to use by wrapping our own code around it. If you want to follow along, [you can find the entire example project on GitHub.](https://github.com/jacksteamdev/runtime-messaging-example)

## Sending a message from a content script

For the content script, let's wrap `chrome.runtime.sendMessage` in a Promise and add it to our injected content script:

```javascript
function sendMessage(message) {
  return new Promise((resolve, reject) => {
    try {
      chrome.runtime.sendMessage(message, resolve);
    } catch (err) {
      reject(err);
    }
  });
}
```

Before we can send a message, we need to make one. A message can be any object that can be converted into JSON, but it usually has a `greeting` property. I like to put an enum object in an `ENUM.js` file to inject along with both my content script and my background scripts, but here we'll just use strings. We can add a `text` property to define what text to set on the browser action badge.

```javascript
const message = { greeting: 'SET_BADGE_TEXT', text: '😀' };
```

Now we can send a message like this, and optionally handle the response using the `then` method.

```javascript
sendMessage(message).then(response => {
    // Log the message sent back from background.js
    console.log('response from background.js:', response);
  });
```

## Receiving a message in the background script
First, we need to make sure we have a background script, so add the following to your `manifest.json` file, if you don't already have a background page or script.

```json
"background": {
  "scripts": ["background.js"]
},
```

The `scripts` property is an array of files that Chrome loads into a background page in order from first to last. They share the same global scope, so that makes using modules easy. Using the `import` keyword in Chrome Extensions can be tricky, so let's just add a second file to our `scripts` array:

```json
"scripts": ["message.bg.js", "background.js"]
```

Now we can create `message.bg.js` and add the following:

```javascript
function listenForMessage(callback) {
  async function asyncCallback(message, sender) {
    // Make sure the callback returns a Promise
    return callback(message, sender);
  }

  function handleMessage(message, sender, sendResponse) {
    asyncCallback(message, sender)
      .then(result =>
        sendResponse({
          success: true,
          greeting: message.greeting,
          ...result,
        }),
      )
      .catch(reason => {
        sendResponse({
          success: false,
          greeting: message.greeting,
          ...reason,
        });
      });

    return true;
  }

  chrome.runtime.onMessage.addListener(handleMessage);
}
```

I won't go into great detail, but at the heart of `listenForMessage` is `chrome.runtime.onMessage`, an event that fires for `any` message sent from `any` tab by the content script injected by your extension.

We can use `listenForMessage` like this in `background.js`:

```javascript
listenForMessage(callbackFn);
```

The first argument of `listenForMessage` is a callback that will receive the message. We can use the following as `callbackFn`:

```javascript
const callbackFn = (message, sender) => {
  switch (message.greeting) {
    case 'SET_BADGE_TEXT':
      console.log('message from content.js:', message);
      chrome.browserAction.setBadgeText({ text: message.text });
      return {};
    default: // do nothing
  }
}
```

Our callback function will take two arguments: `message` and `sender`. We know about `message`, but what is `sender`? It contains details from the browser tab that sent the message.

We can use a `switch` statement to check the `greeting` property and determine what to do with the message. If `greeting` is `SET_BADGE_TEXT`, we log the message to the console for the *background page* and call `chrome.browserAction.setBadgeText`, which takes an options object with one property: `text`.

Then we return an object with the values we want to send back to the content script. Here we don't have anything to say to the content script, so we just send back an empty object. 

`listenForMessage` will handle sending our response for us.  It will add `success: true` to the response object if the operation didn't throw. If there was an error, it will catch the error and send a response with `success: false` and the details of the error.

If our response has no `greeting`, `listenForMessage` will also add the same `greeting` value that was sent from the content script.

Now that the background page has a way to receive our messages, let's try it out! Let's add a simple button to send a message from our content script to our background page ([you can view the entire project on GitHub](https://github.com/jacksteamdev/runtime-messaging-example)):

```javascript
const button = document.createElement('button');
button.innerText = 'Set Badge Text';
button.onclick = handleClick;
document.body.append(button);
```

Load the extension into Chrome from the extensions page or reload it if you've already added your extension. When you reload your test page, the extension will inject the content script and add our button to the bottom of the page. When you click it, the button will send a message to your background page and change the browser action badge!
