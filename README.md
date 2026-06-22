# Smart-Campus-Emergency-Notification-and-Management-System
## 專案簡介
本專案為「智慧校園緊急事件通報與管理系統」，主要利用 Raspberry Pi、GPIO 按鈕、LED、MQTT、Node-RED Dashboard 與 LINE Bot 建立一套校園緊急事件通知系統。

當教室或宿舍發生緊急事件時，使用者可以按下對應的實體按鈕。Raspberry Pi 偵測到按鈕觸發後，會立即點亮對應 LED，並透過 MQTT 將事件資料傳送至 Node-RED Dashboard，同時透過 LINE Bot 發送緊急通知給管理員。管理員處理完成後，可在 Dashboard 按下「事件已解決」按鈕，系統會更新事件狀態並關閉對應 LED。

### 系統架構圖如下

<img width="361" height="641" alt="image" src="https://github.com/user-attachments/assets/951c1429-9080-4ea7-9c89-74bef757d3c9" />


### 在開始執行程式前我們需要先安裝會用到的一些套件  
#### 樹梅派連接方式
先ping rpi5-XX.local(確保連線成功)  
再輸入 “名稱@rpi5-XX.local”，確認密碼並成功連線 

#### 當我們成功連線到樹梅派之後要在終端機輸入以下指令、創建資料夾並進入虛擬環境
cd ~/workspace  
mkdir final (final 為我們自己取的資料夾名稱)  
cd final(進入資料夾)  
python -m venv venv -system-site-packages(創建虛擬環境)  

#### 接下來我們要安裝Node-RED套件，需要輸入的指令如下(終端機不用進入workspace 和虛擬環境)
bash <(curl -sL https://github.com/node-red/linux installers/releases/latest/download/update-nodejs-and-nodered-deb)  
再透過網址打開Node-RED: http://rpi5-XX.local:1880 (XX 可以替換成自己組別)  
如果打不開可以嘗試利用IP address打開，網址如下: http://ip address:1880 (ip address 需替換成自己樹梅派對應的ip address)

#### 再來，我們需要安裝lgpio套件，需要輸入的指令如下(在虛擬環境下)
source venv/bin/activate (進入虛擬環境)  
sudo apt update  
sudo apt install swig liblgpio-dev  
pip install lgpio  
pip list  

#### 同時我們也需要安裝paho-mqtt套件，指令如下(以下兩種方式擇一) 
方法(一): 在樹梅派終端機目標資料夾虛擬環境下  
pip install paho-mqtt  
方法(二): 利用 PC 的 conda 去安裝paho-mqtt，指令如下  
conda create -n paho-mqtt python=3  
conda activate paho-mqtt  
conda install -c conda-forge paho-mqtt

#### 最後需要安裝Line套件(虛擬環境下)  
pip install -upgrade pip  
pip install requests python-dotenv  
pip list

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


去此連結並按照以下步驟去找Channel Access Token 和 User ID  
https://developers.line.biz/en/services/messaging-api/

#### Find Your Channel Access Token 
1. Go to the LINE Developers Console.
2. Click your Provider.
3. Click the Messaging API Channel in your Provider.
4. Click "Messaging API" tab.
5. Scroll down to find the channel access token (long-lived).
6. Click "Issue" button to generate the channel access token.
7.  Now you can copy it and paste it to the .env file.

#### Find Your User ID
1. Go to the LINE Developers Console.
2. Click your Provider.
3. Click the Messaging API Channel in your Provider.
4. Click "Basic Settings" tab.
5. Scroll down to find your user ID.
6.  Now you can copy it and paste it to the .env file.

接下來我們只需要去執行vscode之中Group_16_final.py這個程式再去Node-RED中按部署確認mqtt有順利連接到樹梅派。  


當順利連接到Node-RED之後我們可以到http://rpi5-XX.local:1880/dashboard/page2 這個網站去看我們的Dashboard(其中XX的位址要換成自己組別的樹梅派編號，或是從rpi5到冒號之前可以替換成自己樹梅派的ip address)

### 模擬流程(系統執行流程)
當Dashboard可以順利顯示出未發生事件的畫面時，我們就可以按按鈕來模擬此套系統如何運作。  
首先，我們可以將電路板的對應GPIO27的按鈕按下，此時表示"Dorm發生緊急事件"，而電路板中對應GPIO20的LED也會隨之亮起，且Dashboard和Line Bot也會同時收到Dorm發生緊急事件(包含事件發生時間、地點、設備名稱及事件狀態)Dashboard宿舍欄位也會亮紅燈。

接下來管理員可以開始去處理事件，當處理完成即可按下Dashboard中的"宿舍事件已解決"按鈕，此時電路板的LED燈會隨之熄滅，Dashboard的宿舍事件也會由亮紅燈轉為綠燈  
VS Code終端機則會出現"宿舍事件已解決"的訊息，並包含管理員解決事件的時間、設備、地點等訊息。
