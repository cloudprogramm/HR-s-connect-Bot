## HR's BOT

Selenium bot for parsing IT HR's on Linkedin and send them connect. 

## Installations

* Python3 must be already installed
* cromedriver.exe must be compatible with your driver version
* ```DRIVER_PATH``` in ```params.py``` must refer on your full path to driver

```shell
git clone https://github.com/cloudprogramm/HR-s-connect-Bot.git
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

You must create ```_auth_data.py``` in chromeDriver folder and create your ```EMAIL``` and ```PASSWORD``` from Linkedin!

## Additional

* If you want to find another HR's you have to change ```URL_PARSE``` variable in ```bot_chrome.py```
* Version of chromedriver is 101.0.4951.54
