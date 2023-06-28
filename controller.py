import time
from Views.MessageBoxView import TelegramMessages
from pyrogram import Client, filters
from pyrogram.errors import RPCError, SessionPasswordNeeded
from pyrogram.types import User, TermsOfService
import os
import socket
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
        self.sock = None

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
            print(e)

    def download_from_history(self, chat_name):
        print('started')
        if not self.app:
            self.app = Client(name="app")
            if not self.app.is_connected:
                self.app.start()
        added = []
        members_count = 0
        messages_count = 0
        self.sock = socket.socket()
        self.sock.connect(('localhost', 9090))
        try:
            for message in self.app.get_chat_history(chat_name):
                first_name, last_name, username, user_id, member = self.messages_handler(message)
                messages_count += 1
                self.sock.send(str(messages_count).encode())

                command = self.sock.recv(1024)
                if command.decode() == 'pause':

                    while True:
                        time.sleep(1)
                        command = self.sock.recv(1024)
                        print('paused')
                        if command.decode() == 'resume':
                            print('resumed')
                            break
                        elif command.decode() == 'stop':
                            print('stopped in pause')
                            self.app.stop()
                            self.sock.send('Done'.encode())
                            self.sock.close()
                            self.sock = None
                            return
                elif command.decode() == 'stop':
                    break

                if member not in added:
                    self.download_members_to_files(members_count=members_count, member=member,
                                                   chat_name=chat_name, user_id=user_id)
                    added.append(member)
                    members_count += 1
                    self.sock.send(f'Добавлен участник {member}'.encode())
                else:
                    pass
            self.app.stop()
            self.sock.send('Done'.encode())
            self.sock.close()
            self.sock = None

        except Exception as err:
            print(err)

    def messages_handler(self, message):
        first_name = message.from_user.first_name if message and message.from_user and message.from_user.first_name else ' '
        last_name = message.from_user.last_name if message and message.from_user and message.from_user.last_name else ' '
        username = message.from_user.username if message and message.from_user and message.from_user.username else '.......'
        user_id = message.from_user.id if message and message.from_user and message.from_user.id else '.......'
        member = f'@{username} {first_name} {last_name} ID:{user_id}\n'
        return first_name, last_name, username, user_id, member

    def download_members_to_files(self, members_count, member, chat_name, user_id):
        if not os.path.exists('скачанные файлы'):
            os.makedirs('скачанные файлы')
        with open(f'скачанные файлы/members_{chat_name}.txt', 'a', encoding="utf-8") as file:
            file.seek(0)
            file.write(f'{members_count + 1}. {member}')
            file.truncate()
        with open(f'скачанные файлы/members_ids{chat_name}.txt', 'a', encoding="utf-8") as file:
            file.seek(0)
            file.write(f'{user_id},')
            file.truncate()

    # def pause_handler(self, command):
    #     if command.decode() == 'pause':
    #         print(111)
    #         while True:
    #             time.sleep(1)
    #             command = self.sock.recv(1024)
    #             print('paused')
    #             if command.decode() == 'resume':
    #                 print('resumed')
    #                 break
    #
import datetime
# TARGET = -1001105793906
# @app.on_message(filters.chat(TARGET))
# async def my_handler(client, message):
# print(message)
#
# app.run()