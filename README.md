# ChatPDF
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
  "username": "",
  "api_key": "",
  "loki_key": "",
  "copyttoaster_key": "",
  "OpenAI_API_key": ""
  }
  ```
  **User should fill in values for "username", "api_key", "OpenAI_API_key".**
  
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
