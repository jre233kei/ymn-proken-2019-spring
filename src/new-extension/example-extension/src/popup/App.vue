<template>
  <div>
    <p>Hello world!</p>
  </div>
</template>

<script>
import axios from 'axios';
//axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";

export default {
  data () {
    return {}
  },
  mounted () {
    axios.post('https://g8kwped00b.execute-api.us-east-1.amazonaws.com/production', {
      headers : {
        'Content-Type': 'application/json;charset=UTF-8',
        'Access-Control-Allow-Origin': '*',
        //"Access-Control-Allow-Credentials": "true"
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
      },
      body: {
        "text": '最悪の製品でした。'
      }
    }).then(response => {
      alert('結果: ' + response.data.text);
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
