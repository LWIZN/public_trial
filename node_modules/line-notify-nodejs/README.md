# LINE Notify Node.js

LINE Notify APIのNode.jsライブラリです。

## Install

```
$ npm install line-notify-nodejs
```

## How to Use

1. 下記ページでトークンを発行する
    - https://notify-bot.line.me/my/

2. トークンを使用して通知を送信する

```javascript
const lineNotify = require('line-notify-nodejs')('LINE NOTIFY TOKEN HERE');

lineNotify.notify({
  message: 'send test',
}).then(() => {
  console.log('send completed!');
});
```
