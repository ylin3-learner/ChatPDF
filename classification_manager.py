#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from common import AccountManager, CrawledDataManager
from pprint import pprint
import aiohttp
import json
from time import sleep
import asyncio

url = "https://api.droidtown.co/Loki/Call/"  # 線上版 URL
POST_INTERVAL_SEC = 5

"""
功能：負責與NeuroKumoko分類模型的交互，處理文本數據並生成分類結果。
主要內容：
1. 加載轉換後的文本。
2. 調用NeuroKumoko模型，傳遞文本數據並接收分類結果。
3. 生成文本的分類標簽和大綱。
"""

class NeuroKumokoManager:
    def __init__(self, account_manager, url=None):
        self._account_manager = account_manager
        self.url = url or "https://api.droidtown.co/Loki/Call/"
        self.crawled_data_manager = CrawledDataManager(
            directory="data",
            parser=self
        )
        self.loki_key = None  # 存儲生成的 loki_key

    # Handle the HTTP POST requests. Shared by all other functions to communicate with NeuroKumoko API
    async def _make_request(self, func, data, loki_key=None, use_loki_key=True):
        payload = {
            "username": self._account_manager.username,
            "func": func,
            "data": data
        }
        
        print(f"\npayload: {payload}")

        if use_loki_key:
            loki_key = loki_key or self.loki_key or self._account_manager.loki_key
            if isinstance(loki_key, str) and loki_key:
                payload["loki_key"] = loki_key
            else:
                raise ValueError("Invalid or missing loki_key.")

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as response:
                return await response.json()

    # Create a NeuroKumoko project using the API
    async def create_project(self, project_name, loki_key=None):
        data = {
            "name": project_name,
            "type": "neuro_kumoko"
        }
        response = await self._make_request(
            "create_project", data, loki_key=loki_key, use_loki_key=False)
        loki_key = response.get("loki_key")
        if isinstance(loki_key, str) and loki_key:
            # Update loki_key in account.info
            self._account_manager.update_key("loki_key", loki_key)
            self.loki_key = loki_key  # 存儲生成的 loki_key
            print(f"Updated loki_key: {self.loki_key}")
        else:
            raise ValueError(
                "Failed to retrieve a valid loki_key from the response.")        
        pprint(response)
        return response

    # Add documents to the NeuroKumoko project
    async def add_documents(self, filename=None):
        # Get parsed content from CrawledDataManager
        documents = self.crawled_data_manager.parse_content(
            filename=filename)

        print(f"document type: {type(documents)}")

        data = {"document": documents}

        print("Data start from here: \n")
        # print(data)
        # Check if data is properly formatted
        response = await self._make_request("insert_document", data)
        # pprint(response)
        return response

    # Deploy the model for the NeuroKumoko project
    async def deploy_model(self):
        response = await self._make_request("deploy_model", {})
        pprint(response)
        return response

    # Check the deployment status of the model
    async def check_model_status(self):
        response = await self._make_request("check_model", {})
        pprint(response)
        return response

    # Retrieve detailed information about the deployed model
    async def get_model_info(self):
        response = await self._make_request("get_info", {})

        # test
        #response = {
            #"msg": "Model is deploying...",
            #"progress_status": "processing",
            #"status": "true"
        #}
        
        # pprint(response)
        return response

    # Get text similarity using the Loki API
    async def get_loki_text_sim(self, input_str, loki_key=None, keyword_list=[], feature_list=["feature_time", "feature_unit", "feature_noun",
            "feature_verb", "feature_location", "feature_person"], count=1):
        payload = {
            "username": self._account_manager.username,
            "loki_key": loki_key,
            "input_str": input_str,
            "keyword": keyword_list,
            "feature": feature_list,
            "count": count
        }

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post("https://api.droidtown.co/Loki/API/", json=payload) as response:
                    if response.status == 200:
                        try:
                            result = await response.json()
                            if result["status"]:
                                if result["progress_status"] == "processing":
                                    await asyncio.sleep(POST_INTERVAL_SEC)
                                    continue
                            return result
                        except Exception as e:
                            return {"status": False, "msg": str(e)}
                    else:
                        return {"status": False, "msg": "HTTP {}".format(response.status)}

    async def build_model(self, project_name):
        await self.create_project(project_name)
        await self.add_documents()
        await self.deploy_model()
        await self.check_model_status()
        await self.get_model_info()

    async def poll_model_status(self, project_name, delay=5, max_retries=10):
        retries = 0

        label_dict = (await self.get_model_info()).get("result", {}).get("label", {})

        # Print the label_dict for debugging
        print("Label dictionary:", label_dict)
        
        label_count = len(label_dict)
        if label_count < 2:
            print("Build Model! document_count should larger than 2!")
            await self.build_model(project_name)
            return False

        progress_status = (await self.check_model_status()).get("progress_status")
        while progress_status != "completed" and retries < max_retries:
            retries += 1
            await asyncio.sleep(delay)
            
            progress_status = (await self.check_model_status()).get("progress_status")

            if retries == max_retries:
                print("Max retries reached. Exiting poll.")
                return False

        return True

    def extract_lexicon_values(self, response_data):

        # check if response_data contains 'result_list', make sure is a list
        if 'result_list' in response_data and isinstance(response_data['result_list'], list):
            for item in response_data['result_list']:
                # check each item in result_list if contains 'lexicon'
                if 'lexicon' in item:
                    return item['lexicon']
        return None

#if __name__ == "__main__":
    #account_manager = AccountManager(filename="config/account.info")
    #neurokumoko_manager = NeuroKumokoManager(account_manager)
    #neurokumoko_manager.create_project("PDF_classfication")
    #flag = await self.neurokumoko_manager.poll_model_status("PDF_classfication")
    #extracted_text = "2024 年巴黎奧運揭幕花都聚集了來自全球各地的運動員和爭睹頂級賽事的觀眾然而這卻讓部分巴黎居民心生怨懟近幾個月來社群媒體可見到部分巴黎民眾對法國首都的狀態抱怨連連有些居民形容巴黎正成為人間地獄警告遊客千萬別來相較於巴黎市政府堅稱奧運取得巨大成功為何巴黎人反而成群結隊地想逃離這座城市訂閱年方案享雙重好禮前100 位加贈電子書 抽日本雙人來回機票還不是會員 馬上註冊  立即搶購巴黎奧運儼然成為巴黎市長伊達戈與總統馬克宏明爭暗鬥的擂臺開幕典禮上馬克宏以東道主身分站C 位開幕前一周伊達戈縱身躍入塞納河證明水質符合奧運標準替巴黎奧運做了最佳宣傳馬克宏不落人後派出體育部長跟進再次掛保證伊達戈究竟是何許人馬克宏為何這麼在意她2024 年巴黎奧運在法國當地時間晚間7 時30 分正式登場開幕式首度搬到塞納河上舉行聖火由法國3 屆奧運柔道金牌得主希內與田徑名將佩雷克共同點燃隨後聖火台藉氫氣球冉冉升空直到閉幕為止巴黎奧運開幕式今晚（台灣時間27 日凌晨1 時30 分）在塞納河登場四度參賽的女子羽球選手戴資穎、首度站上奧運殿堂的霹靂舞選手孫振將共同擔任掌旗官帶領台灣代表團入場24 歲的孫振在取得巴黎奧運霹靂舞資格後不僅成為各界關注焦點也讓霹靂舞（Breaking）這項年輕人熟悉、但對奧運來說相對陌生的新項目映入觀眾眼簾四年一度的奧運在法國巴黎舉行迎接這項全球最大的運動盛會自然也多了許多「一月運動迷」因此衍生出來的商機更不容小覷由於民眾觀看賽事的需求與欲望比平常更為強烈超商、百貨都祭出不少優惠電商也表示有特定商品買氣大漲...法國7 月7 日舉行國會大選選後新國會呈現左中右三派鼎立席次最多的左翼聯盟要求組閣內部卻分裂無法推出總理人選而總統馬克宏上周接受總理艾塔爾帶領的內閣總辭卸任政府繼續看守負責日常事務但無法提出重大政策眼見巴黎奧運即將在7 月26 日開幕法國政局卻陷入癱瘓民眾抱怨生活成本危機但不知道要等到那一天才會有個像樣的新政府提出因應對策...巴黎奧運將於7 月26 日登場但另一場以長壽為主題的「回春奧運」已如火如荼展開主辦者是「健康來得及」曾報導的科技狂人強生（Bryan Johnson）他年砸數百萬美元進行各種療法與長壽飲食想延緩衰老他還積極將此推廣為運動吸引多達8000 名健康狂熱者一同較量比的是用生理年齡檢測看誰身體衰老速度最慢有趣的是花大錢養生的強生沒能稱霸自己的比賽那些贏過他的「民間高手」是怎麼做到的木匠一個看似消失中的行業能引領精彩人生美國木匠席爾佛（Hank Silver）不久前從波士頓機場出境安檢人員起初好奇他如何拿工作簽證出國聽到他的回答卻肅然起敬他是巴黎聖母院重建修復團隊的國際成員席爾佛並非來自傳統木工家庭他的真實人生是在哪一步轉了彎且朝他心目中「千載難逢」的機會邁進邀請您與聯合報數位版攜手走入國際新聞的世界並檢驗您對全球議題的洞察力2024 巴黎奧運的準備已到最後階段4 年一度的體育盛會即將展開開幕式將乘船入場的選手無不摩拳擦掌期待能從塞納河划向最終勝利的頒獎台聯合報每月企畫「新聞時光機」本次將帶領讀者回顧過往奧運中華健兒的精采故事巴黎奧運柔道男子60公斤級賽事我國好手楊勇緯在16 強賽黃金得分賽險勝卡利諾（Andrea Carlino）後8 強賽則是遭遇強敵哈薩克好手斯梅托夫（Yeldos Smetov）的挑戰最終斯梅托夫以半勝優勢取得4 強門票楊勇緯則落入敗部復活賽仍有機會挑戰銅牌 "
    #if flag:
        #print(f"neurokumoko_manager.loki_key: {
              #self.neurokumoko_manager.loki_key}")
        #res = self.neurokumoko_manager.get_loki_text_sim(
            #extracted_text, loki_key=self.neurokumoko_manager.loki_key)
        #print(res)    


            



