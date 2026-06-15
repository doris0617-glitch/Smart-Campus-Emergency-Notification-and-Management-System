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

接下來我們只需要去執行vscode之中Group_16_final.py這個程式再去Node-RED中按部屬確認mqtt有順利連接到樹梅派
當順利連接到Node-RED之後我們可以到http://rpi5-**.local:1880/dashboard/page2 這個網站去看我們的Dashboard
(其中*的位址要換成自己組別的樹梅派編號，或是從rpi5到冒號之前可以替換成自己樹梅派的ip address)

當Dashboard可以順利顯示出未發生事件的畫面時，我們就可以按按鈕來模擬此套系統如何運作
首先，我們可以將電路板的對應GPIO27的按鈕按下，此時表示"Dorm發生緊急事件"，而電路板中對應GPIO20的LED也會隨之亮起
且dashboard和Line Bot也會同時收到Dorm發生緊急事件(包含發生時間、地點、設備名稱及事件狀態)dashboard宿舍欄位也會亮紅燈
接下來管理員可以開始去處理事件，當處理完成即可按下Dashboard中的"宿舍事件已解決"按鈕，此時電路板的LED燈會隨之熄滅，Dashboard的宿舍事件也會由亮紅燈轉為綠燈
vscode終端機則會出現"宿舍事件已解決"的訊息，並包含時間、設備、地點等訊息
