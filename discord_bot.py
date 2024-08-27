#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
功能：負責處理與Discord bot的交互，管理用戶輸入輸出，協調其他模塊。
主要內容：
1. 接收用戶上傳的PDF文件。
2. 調用pdf_handler.py進行PDF文本轉換。
3. 調用classification_manager.py和clustering_manager.py進行文本分類和分群。
4. 處理用戶問題，調用question_answering_manager.py生成答案。
將結果返回給用戶。
"""

import logging
import discord
import json
import os
from pdf_handler import PDFHandler  # Import your PDFHandler class
from main import main
from classification_manager import NeuroKumokoManager
from copyToaster_manager import CopyToasterManager
from common import AccountManager
from chatbotMaker import ConversationManager
import multiprocessing
import sys
import asyncio

logging.basicConfig(level=logging.DEBUG)
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

class BotClient(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        # Save file's last modified time
        self.file_mod_times = {}

        # message's last modified content and time
        self.message_mod_times = {}
        self.message_contents = {}
        
        # Initialize AccountManager instance in this cls should be binded with "self"
        self.account_manager = AccountManager(filename="config/account.info")
        self.neurokumoko_manager = NeuroKumokoManager(self.account_manager)
        self.conversation_manager = ConversationManager(self.account_manager)
     
        # Call main() when BotClient is initialized
        target_urls = [
            "https://house.udn.com/house/index",
            "https://udn.com/news/cate/2/7225"
        ]
        filenames = ["house", "international_media"]
        
        for target_url, filename in zip(target_urls, filenames):
            main(target_url, filename, limit=1)

        # Initialize copyToasterManager instance
        self.copyToater_manager = CopyToasterManager(self.account_manager)

    async def on_ready(self):
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        # Print user's message content
        print(f'User Message: {message.content}')

        # Check if message is unknown
        if message.id in self.message_mod_times:
            last_mod_time = self.message_mod_times[message.id]
            if message.content != self.message_contents[message.id] or last_mod_time != message.created_at.timestamp():
                # Update message record and handle message content
                self.message_mod_times[message.id] = message.created_at.timestamp()
                self.message_contents[message.id] = message.content
                await message.reply('Message has been updated.')
            else:
                return  # If not, ignore
    
        else:
            # record the updated message content and time
            self.message_mod_times[message.id] = message.created_at.timestamp()
            self.message_contents[message.id] = message.content        

        # Check if the message contains any attachments
        if message.attachments:
            for attachment in message.attachments:
                # Check if the attachment is a PDF file
                if attachment.filename.endswith('.pdf'):
                    # Save the PDF file to a temporary location
                    save_path = os.path.join(data_dir, attachment.filename)
                    await attachment.save(save_path)
                    
                    # Get the current modified time
                    current_mod_time = os.path.getmtime(save_path)
                            
                    await message.reply(f'Received PDF: {attachment.filename}')
                    if (attachment.filename not in self.file_mod_times or
                            self.file_mod_times[attachment.filename] != current_mod_time):

                        # Update the file's modified time
                        self.file_mod_times[attachment.filename] = current_mod_time
                        # Process the PDF file using pdf_handler
                        pdf_handler = PDFHandler(save_path)
                        extracted_text = pdf_handler.extract_text()

                        # Optionally, reply to the user with a confirmation or some text
                        await message.reply(f'Text extracted from {attachment.filename}.')

                        await self.neurokumoko_manager.create_project(
                            "PDF_classfication")
                        flag = await self.neurokumoko_manager.poll_model_status("PDF_classfication")
                        if flag:
                            print(f"neurokumoko_manager.loki_key: {
                                  self.neurokumoko_manager.loki_key}")
                            res = await self.neurokumoko_manager.get_loki_text_sim(
                                extracted_text, loki_key=self.neurokumoko_manager.loki_key)
                            print(res)
                            
                            # print(f'Extracted Text from {attachment.filename}:')
                            lexicon_values = await self.neuroKumoko_manager.extract_lexicon_values(res)
                            if lexicon_values:
                                await message.reply(f"Your PDF seem to belong to {sim}!")

                                # Call CopyToaster to get clustering_result
                                response_data = self.copyToater_manager.getCopyToasterResult(
                                    lexicon_values, extracted_text)
                                similarity_documents = self.copyToater_manager.extract_category_documents(
                                    response_data)
                                print(similarity_documents)
                                
                                # Call ConversationManager and set similarity_documents
                                self.conversation_manager.insert_data(
                                    similarity_documents=similarity_documents)

                                # Retrieve and update message content dynamically
                                message_content = self.get_message_content(
                                    message)
                                response = self.conversation_manager.generate_response(
                                    message_content)
                                await message.reply(response)
                                
                            else:
                                await message.reply(f"Oops! There is no matched category for the current bot!\n Wait for bot to handle...")
                        else:
                            await message.reply(
                                "Model is building... Please try again in an hour.")
                            sys.exit(0)

    def get_extracted_text(self, filename):
        return self.extracted_texts.get(filename, None)

    def get_message_content(self, message):
        return message.content


if __name__ == "__main__":
    try:
        with open("config/account.info", encoding="utf-8") as f:  # Read account.info
            accountDICT = json.loads(f.read())
    
        intents = discord.Intents.default()
        intents.message_content = True  # Ensure the bot can read message content
    
        client = BotClient(intents=intents)
        client.run(accountDICT["discord_token"])
    except discord.errors.PrivilegedIntentsRequired as e:
        logging.error(f"Privileged intents required: {e}")
    except discord.errors.LoginFailure as e:
        logging.error(f"Login failed: {e}")
    except discord.errors.ConnectionClosed as e:
        logging.error(f"Connection closed: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")    
