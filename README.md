# Smart-Campus-Emergency-Notification-and-Management-System
AIoT emergency notification system using Raspberry Pi, Node-RED, and LINE Bot.
。倉庫中需包含README說明，讓讀者能夠根據說明來安裝與
執行你們的物聯網應用。

我們所設計的期末專題是智慧校園緊急事件通報與管理系統
總共有3個上傳的檔案，分別是Group_16_final.py、empty.env、flows.json三個檔案
首先我們可以將Grpup_16.py與empty.env這兩個檔案載入到vscode中，再將flows.json載入到Node-RED中

其中empty.env之中會有兩行程式如下
LINE_CHANNEL_ACCESS_TOKEN=在這裡貼上你的長期 token
LINE_USER_ID=在這裡貼上你的測試用 userId 或群組 Id
我們需要按照授課講義第10章的 https://developers.line.biz/en/services/messaging-api/這個連結
並參照講義11-12頁的步驟去找尋自己的長期的token跟userId

接下來我們只需要去執行vscode之中Group_16_final.py這個程式再去Node-RED中按部屬確認mqtt友順利連接到樹梅派
