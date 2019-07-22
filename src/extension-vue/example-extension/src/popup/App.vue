<template>
  <div></div>
</template>

<script>
import axios from 'axios';

/*
//axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";

window.addEventListener('load', (event) => {
  chrome.tabs.executeScript(null, {
    file: '../content.js', //my content script
  }, () => {
    connect() //this is where I call my function to establish a connection
  });
});

function connect () {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const port = chrome.tabs.connect(tabs[0].id);
    port.postMessage({ function: 'html' });
    port.onMessage.addListener((response) => {
      html = response.html;
      title = response.title;
      description = response.description;
    });
  });
}
*/

export default {
  data () {
    return {}
  },
  mounted () {

    /*
    axios.post('https://g8kwped00b.execute-api.us-east-1.amazonaws.com/production', {
      headers : {
        'Content-Type': 'application/json;charset=UTF-8',
        'Access-Control-Allow-Origin': '*',
        //"Access-Control-Allow-Credentials": "true"
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
      },
      body: {
        "text": "最悪の製品でした。"
      }
    }).then(response => {
      alert('結果: ' + response.data.text);
    }).catch(error => {
      alert(error);
    });;
    */






    axios.post('https://g8kwped00b.execute-api.us-east-1.amazonaws.com/production', {
      text: "最悪な商品でした。返品したいです！"
    }).then(response => {
      console.log(response["data"]["body"]);
      //alert('結果: ' + response["data"]["body"]);
    }).catch(error => {
      alert(error);
    });;


  }

}
</script>

<style lang="scss" scoped>
p {
  font-size: 20px;
}
</style>
