#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from common import AccountManager, CrawledDataManager
from requests import post
from pprint import pprint
import requests
import json
from time import sleep


url = "https://api.droidtown.co/CopyToaster/Call/"
POST_INTERVAL_SEC = 5

class CopyToasterManager:
    def __init__(self, account_manager, url=None):
        self._account_manager = account_manager
        self.url = url or "https://api.droidtown.co/CopyToaster/Call/"

    def _make_request(self, func, data=None, category_name=None, use_copytoaster_key=True):
        payload = {
            "username": self._account_manager.username,
            "func": func,
            "data": data
        }
        
        if category_name is not None:
            payload["category"] = category_name

        print(f"\n{payload}")

        if use_copytoaster_key:
            copytoaster_key = self._account_manager.copytoaster_key
            if isinstance(copytoaster_key, str) and copytoaster_key:
                payload["copytoaster_key"] = copytoaster_key
            else:
                raise ValueError("Invalid or missing copytoaster_key.")

        response = post(self.url, json=payload)
        return response.json()

    def create_project(self, project_name):
        data = {
            "name": project_name,
        }
        response = self._make_request(
            "create_project", data, use_copytoaster_key=False)
        copytoaster_key = response.get("copytoaster_key")
        if isinstance(copytoaster_key, str) and copytoaster_key:
            # 更新 account_gs.info 文件中的 loki_key
            self._account_manager.update_key(
                "copytoaster_key", copytoaster_key)
        else:
            raise ValueError(
                "Failed to retrieve a valid copytoaster_key from the response.")
        pprint(response)
        return response
    
    def create_category(self, category_name):
        print(f"Creating category for category_name: {category_name}")

        # Make request to create category
        response = self._make_request(
            "create_category", category_name=category_name, data={})
        pprint(response)    

    def add_documents(self, source, category_name):
        print(f"Adding documents to the category")
    
        # Assume source is the parsed content you want to add as documents
        documents = source
    
        print(f"Document type: {type(documents)}")
        data = {"document": documents}
        #data = {"document": [
            #{'title': 'cluster_41', 'content': '未來一年借房貸恐變難...交報告後還有這關 銀行圈 這次楊金龍是玩真的', 'hashtag': []}]}
    
        # print(f"\n{data}")
        # Make request to insert documents
        response = self._make_request(
            "insert_document", data=data, category_name=category_name)
        pprint(response)

    # Deploy the model for the NeuroKumoko project
    def deploy_model(self):
        response = self._make_request("deploy_model", {})
        pprint(response)
        return response

    # Check the deployment status of the model
    def check_model_status(self):
        response = self._make_request("check_model", {})
        pprint(response)
        return response

    # Retrieve detailed information about the deployed model
    def get_model_info(self):
        response = self._make_request("get_info", {})
        pprint(response)
        return response

    def build_model(self, filename, source):
        self.create_project("PDF_Answers")
        self.create_category(filename)
        self.add_documents(source, filename)
        self.deploy_model()
        self.check_model_status()
        self.get_model_info()

    def getCopyToasterResult(self, categorySTR, inputSTR, count=15):
        payloadDICT = {
            "username": self._account_manager.username,
            "copytoaster_key": self._account_manager.copytoaster_key,
            "category": categorySTR,
            "input_str": inputSTR,
            "count": count
        }
    
        while True:
            response = post(COPYTOASTER_URL, json=payloadDICT)
            if response.status_code == 200:
                try:
                    resultDICT = response.json()
                    if resultDICT["status"]:
                        if resultDICT["progress_status"] == "processing":
                            sleep(POST_INTERVAL_SEC)
                            continue
                    return resultDICT
                except Exception as e:
                    return {"status": False, "msg": str(e)}
            else:
                return {"status": False, "msg": "HTTP {}".format(response.status_code)}

    def extract_category_documents(self, response_data):

        # check if response_data contains 'result_list', make sure is a list
        if 'result_list' in response_data and isinstance(response_data['result_list'], list):
            for item in response_data['result_list']:
                # check each item in result_list if contains 'lexicon'
                if 'document' in item:
                    raw_document = item['document']
                    if "\n" in raw_document:
                        return document.split("\n", 1)[1]
                    return raw_document
    
        return None    

