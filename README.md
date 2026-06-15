# Smart-Campus-Emergency-Notification-and-Management-System
## 專案簡介
本專案為「智慧校園緊急事件通報與管理系統」，主要利用 Raspberry Pi、GPIO 按鈕、LED、MQTT、Node-RED Dashboard 與 LINE Bot 建立一套校園緊急事件通知系統。

當教室或宿舍發生緊急事件時，使用者可以按下對應的實體按鈕。Raspberry Pi 偵測到按鈕觸發後，會立即點亮對應 LED，並透過 MQTT 將事件資料傳送至 Node-RED Dashboard，同時透過 LINE Bot 發送緊急通知給管理員。管理員處理完成後，可在 Dashboard 按下「事件已解決」按鈕，系統會更新事件狀態並關閉對應 LED。


### 在開始執行程式前我們需要先安裝會用到的一些套件

<img width="527" height="262" alt="image" src="https://github.com/user-attachments/assets/e5ace9db-757d-4795-bc52-8b12edcf9e18" />
<img width="586" height="203" alt="image" src="https://github.com/user-attachments/assets/495a31a7-c579-4121-bd8a-9c01b6d34203" />
<img width="647" height="217" alt="image" src="https://github.com/user-attachments/assets/ac835c28-8c71-41f6-a667-94b689a5b19b" />
<img width="341" height="177" alt="image" src="https://github.com/user-attachments/assets/037e8510-09bd-4c7b-bc70-14e13df12b15" />


### GPIO接腳如下

<img width="502" height="383" alt="image" src="https://github.com/user-attachments/assets/c9757fd7-2e2c-4079-8d53-c198a2705c4e" />

### 電路圖與LED, Button所對應的接腳

<img width="518" height="432" alt="image" src="https://github.com/user-attachments/assets/e75bb0a5-f4b1-4408-98be-1e357328bbe5" />


### 開始匯入檔案
總共有3個上傳的檔案，分別是Group_16_final.py、empty.env、flows.json三個檔案
首先我們可以將Grpup_16.py與empty.env這兩個檔案載入到vscode中，再將flows.json載入到Node-RED中


其中empty.env之中會有兩行程式如下（使用時請將黨名由empty.env改成.env）

LINE_CHANNEL_ACCESS_TOKEN=在這裡貼上你的長期 token

LINE_USER_ID=在這裡貼上你的測試用 userId 或群組 Id

可以參照以下的指令步驟去找尋Channel access token和user id

<img width="785" height="437" alt="image" src="https://github.com/user-attachments/assets/9535a6be-728a-422e-b695-a2c70e1a20c9" />
<img width="680" height="425" alt="image" src="https://github.com/user-attachments/assets/a3c54bd3-a09f-4c9c-bd0c-7ca0b0b56bdf" />


接下來我們只需要去執行vscode之中Group_16_final.py這個程式再去Node-RED中按部署確認mqtt有順利連接到樹梅派，當順利連接到Node-RED之後我們可以到http://rpi5-XX.local:1880/dashboard/page2 這個網站去看我們的Dashboard(其中XX的位址要換成自己組別的樹梅派編號，或是從rpi5到冒號之前可以替換成自己樹梅派的ip address)

### 模擬流程(系統執行流程)
當Dashboard可以順利顯示出未發生事件的畫面時，我們就可以按按鈕來模擬此套系統如何運作。首先，我們可以將電路板的對應GPIO27的按鈕按下，此時表示"Dorm發生緊急事件"，而電路板中對應GPIO20的LED也會隨之亮起，且dashboard和Line Bot也會同時收到Dorm發生緊急事件(包含發生時間、地點、設備名稱及事件狀態)dashboard宿舍欄位也會亮紅燈。

接下來管理員可以開始去處理事件，當處理完成即可按下Dashboard中的"宿舍事件已解決"按鈕，此時電路板的LED燈會隨之熄滅，Dashboard的宿舍事件也會由亮紅燈轉為綠燈
vscode終端機則會出現"宿舍事件已解決"的訊息，並包含時間、設備、地點等訊息。
