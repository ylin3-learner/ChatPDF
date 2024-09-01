# Docky-Talky
## Overview
##### This repository is an application similar to ChatPDF; however, implement it in a different way based on [LokiHub](https://github.com/Droidtown/LokiHub)
##### It addresses to tackle hallucination of ChatPDF when directly calling ChatGPT API.
- It uses three modules for the uploaded PDF and find the simliarest document inside the modules.
  - create category [NeuroKumoko of LokiHub](https://github.com/Droidtown/LokiTool_Doc/wiki/15_Func_Create_Project_NeuroKumoko)
  - cluster documents [GreedySLime of LokiHub](https://github.com/Droidtown/LokiTool_Doc/wiki/16_Func_Create_Project_GreedySlime)
  - return the simliarest documents based on category [CopyToaster of LokiHub](https://api.droidtown.co/document/#CopyToaster)
- After getting the similarest docuements, use the result to call ChatGPT to get the most related result based on your query and uploaded PDF.

## Instructions
### 1. clone this project to your local repository
  ### Prerequisites
  - Ensure that [Git](https://git-scm.com/downloads) is installed on your local computer.
  - You should have access to the repository you want to clone (either public or private with appropriate credentials).
  ### Cloning a Repository
  1. Open Terminal or Command Prompt:
  - On Windows: You can use Git Bash, Command Prompt, or any terminal emulator like PowerShell.
  - On Mac/Linux: Open the Terminal application.
  2. Navigate to the Directory Where You Want to Clone the Repository: Use the cd command to move to your desired directory. For example:
  ```
  cd path/to/your/folder
  ```
  3. Run the git clone Command here: Use the git clone command followed by the URL of the repository you want to clone. 
  ```
  git clone https://github.com/ylin3-learner/ChatPDF.git
```

### 2. Add an *account.info* file in the *config* folder, and its format will be like:
  ```
  {
  "discord_token": "",
  "username": "",
  "api_key": "",
  "loki_key": "",
  "copyttoaster_key": "",
  "OpenAI_API_key": ""
  }
  ```
  **User should fill in values for "username", "api_key", "OpenAI_API_key", "discord_token"**
  ##### For "discord_token":
  - 1. *Create a Discord Account*: If you haven't already, create an account on Discord.
    2. *Go to the Discord Developer Portal*: Visit the Discord Developer Portal.
    3. *Create a New Application:*
       - Click on the "New Application" button.
       - Enter a name for your application (this can be anything you like).
       - Click "Create".
    4. *Create a Bot:*
       - After creating the bot, you will see a "Token" section on the Bot page.
       - Click "Copy" under the "Token" section to copy your bot's token to your clipboard.
       - Note: Keep this token secret! It is essentially the password for your bot and allows it to authenticate with Discord.
    5. *Enable Privileged Gateway Intents (if needed):*
       - If your bot requires access to certain events, such as member updates or presence updates, scroll down to the "Privileged Gateway Intents" section and toggle the "Presence Intent" and "Server Members Intent" options as needed.
    6. *Invite Your Bot to a Server:*
       - Go to the "OAuth2" tab on the left.
       - Under "OAuth2 URL Generator," select the "bot" scope and assign the permissions your bot needs.
       - Copy the generated URL and paste it into your browser. Then, select a server to add your bot to.
  ##### For "username" and "api_key":
  - Go to the [LokiHub website](https://api.droidtown.co/login/) and click on *"註冊"* or *"Register"* to get your *username* and *api_key*, which is the account you apply to.
  
  ##### For "OpenAI_API_key":
  - Go to [ChatGPT website](https://platform.openai.com/docs/api-reference/introduction) to sign up or login to get your "OpenAI_API_key"'s value

**No need to fill in "loki_key"'s value and "copytoaster_key"'s value, which will be automatically generated.**

## 3. The repository may rely on some libraries, run
```
pip install -r requirements.txt
```

## 4. After you've done above, run *discord_bot.py* and the whole program will start running.

## Directory
```
.
├── .gitignore                   # Git 忽略文件設定
├── discord_bot.py               # Discord Bot 主程式文件
├── LICENSE                      # 授權文件
├── README.md                    # 專案說明文件
├── requirements.txt             # Python 相依套件列表
├── config/                      # 配置文件目錄
│   ├── account.info             # 帳戶相關信息
│   └── crawled_links.json       # 已爬取連結記錄
├── data/                        # 數據目錄
│   ├── house.json               # 房地產數據
│   └── international_media.json # 國際媒體數據
├── NLU/                         # 自然語言理解模塊目錄
│   ├── chatbotMaker.py          # 聊天機器人生成器
│   ├── classification_manager.py# 分類管理器
│   ├── clustering_manager.py    # 聚類管理器
│   ├── common.py                # 通用功能
│   ├── copyToaster_manager.py   # 文案管理器
│   └── __init__.py              # 包初始化文件
├── PDF/                         # PDF 相關處理模塊目錄
│   ├── pdf_handler.py           # PDF 處理器
│   └── __init__.py              # 包初始化文件
└── Scraper/                     # 網頁爬蟲模塊目錄
    ├── clicker.py               # 點擊模塊
    ├── parser.py                # 解析模塊
    ├── recorder.py              # 紀錄器模塊
    ├── scraper_main.py          # 爬蟲主程式
    └── __init__.py              # 包初始化文件
```
## Contacts
### Email: husenior11123@gmail.com
