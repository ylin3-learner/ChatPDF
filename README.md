# ChatPDF
## Overview
##### This repository is an application similar to ChatPDF; however, implement it in a different way based on [LokiHub](https://github.com/Droidtown/LokiHub)
- It addresses to tackle hallucination of ChatPDF when directly calling ChatGPT API.
- It uses three modules for the uploaded PDF and find the simliarest document inside the modules.
  - create category [NeuroKumoko of LokiHub](https://github.com/Droidtown/LokiTool_Doc/wiki/15_Func_Create_Project_NeuroKumoko)
  - cluster documents [GreedySLime of LokiHub](https://github.com/Droidtown/LokiTool_Doc/wiki/16_Func_Create_Project_GreedySlime)
  - return the simliarest documents based on category [CopyToaster of LokiHub](https://api.droidtown.co/document/#CopyToaster)
- After getting the similarest docuements, use the result to call ChatGPT to get the most related result based on your query and uploaded PDF.

## Instructions

