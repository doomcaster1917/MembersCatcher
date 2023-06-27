import time
from Views.MessageBoxView import TelegramMessages
from pyrogram import Client, filters
from pyrogram.errors import RPCError, SessionPasswordNeeded
from pyrogram.types import User, TermsOfService
import os
from functools import wraps
import asyncio
import os.path
import logging
import sqlite3

logging.basicConfig(level=logging.ERROR)

# telegram_sign_in(api_id=28961703, api_hash="e4335a60701cdfa994f9891270936910",
# phone='+79106659144', account_name='@LeninOxuenen')"@elektro_velo_servis"

def check_session_exists():

    if os.path.isfile('app.session'):
        try:
            con = sqlite3.connect("app.session")
            cur = con.cursor()
            res = cur.execute("SELECT user_id FROM sessions").fetchone()
            cur.close()
            if res[0]:
                return True
            else:
                return False
        except Exception as e:
            logging.error(e)
    else:
        return False


def telegram_sign_in(api_id, api_hash, phone, account_name) -> User:
    app = Client(name= "app", api_id=api_id, api_hash=api_hash, test_mode=False)


    try:
        app.connect()
        sent_code = app.send_code(phone)
        print('The code has been sent')
        code = TelegramMessages.telegram_auth_code()

        try:
            signed_in = app.sign_in(phone, sent_code.phone_code_hash, code)

            if isinstance(signed_in, User):
                return signed_in

        # 4.5 In case 2FA is enabled
        except SessionPasswordNeeded:
            app.check_password(TelegramMessages.telegram_auth_code(two_factor=True))

        # 5. If new user, Client sign up ✅
        signed_up = app.sign_up(phone, sent_code.phone_code_hash, account_name)

        # 6. If new user, Client accept terms of service
        if isinstance(signed_in, TermsOfService):
            app.accept_terms_of_service(signed_in.id)

        return signed_up

    except RPCError as e:
        logging.error(e)

        raise e


class TelegramApi():

    def __init__(self):
        self.app = None

    def get_chat_name(self, chat_id):
        try:
            if not self.app:
                self.app = Client(name="app")
                self.app.start()

            chat = self.app.get_chat(chat_id)

            if chat.title:
                self.app.stop()
                self.app = None
                return chat.title
        except Exception as e:
            pass

    async def download_from_history(self, chat_name):
        if not self.app:
            self.app = Client(name="app")
            if not self.app.is_connected:
                await self.app.start()
        added = []
        chat_id = chat_name
        count = 0
        try:
            async for message in self.app.get_chat_history(chat_id):
                first_name = message.from_user.first_name if message and message.from_user and message.from_user.first_name else ' '
                last_name = message.from_user.last_name if message and message.from_user and message.from_user.last_name else ' '
                username = message.from_user.username if message and message.from_user and message.from_user.username else '.......'
                user_id = message.from_user.id if message and message.from_user and message.from_user.id else '.......'
                member = f'@{username} {first_name} {last_name} ID:{user_id}\n'
                if member not in added:
                    if not os.path.exists('скачанные файлы'):
                        os.makedirs('скачанные файлы')
                    with open(f'скачанные файлы/members_{chat_id}.txt', 'a', encoding="utf-8") as file:
                        file.write(f'{count + 1}. {member}')
                    with open(f'скачанные файлы/members_ids{chat_id}.txt', 'a', encoding="utf-8") as file:
                        file.write(f'{user_id},')
                    added.append(member)
                    count += 1
                    yield f'Добавлен участник {member}'
                else:
                    pass
            await self.app.stop()
            print('Загрузка завершена')
        except Exception as err:
            raise err


import datetime
# TARGET = -1001105793906
# @app.on_message(filters.chat(TARGET))
# async def my_handler(client, message):
# print(message)
#
# app.run()