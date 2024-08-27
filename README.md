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
- clone this project to your local repository
```
git clone "repository of this repo"
```
- add an *account.info* file in the *config* folder, and its format will be like:
```
{
"username": "",
"api_key": "",
"loki_key": "",
"copyttoaster_key": "",
"OpenAI_API_key": ""
}
```
- Go to the [LokiHub website](https://api.droidtown.co/) to get your username and api_key, which is the account you apply to.
- **No need to fill in "loki_key"'s value and "copytoaster_key"'s value. Just leave it there as shown above.**
- Go to [ChatGPT website](https://platform.openai.com/docs/api-reference/introduction) to sign up or login to get your "OpenAI_API_key"'s value
- The repository may rely on some libraries: **pytesseract for OCR, OpenAI for ChatGPT, selenium for Web scraper**
```
pip install pytesseract --user
```
```
pip install openAI --user
```
```
pip install selenium --user
```
- After you've done above, directly run discord_bot.py and the whole program will start running.
## Graph package
