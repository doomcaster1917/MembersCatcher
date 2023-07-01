import time
from Views.MessageBoxView import TelegramMessages
from pyrogram import Client, filters
from pyrogram.errors import RPCError, SessionPasswordNeeded
from pyrogram.types import User, TermsOfService
from pyrogram.handlers import MessageHandler
from pathlib import Path
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
        self.already_added = []
        self.chat_name = None
        self.monitoring_messages_count = 0
        self.monitoring_add_members_count = 0

    def get_chat_info(self, chat_name: str):
        try:
            if not self.app:
                self.app = Client(name="app")
                self.app.start()

            chat = self.app.get_chat(chat_name)

            if chat.title:
                self.app.stop()
                self.app = None
                return {'title': chat.title, 'id': chat.id}

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
            if not os.path.exists('скачанные файлы'):
                os.makedirs('скачанные файлы')
            with open(f'скачанные файлы/members_{chat_name}.txt', 'w', encoding="utf-8") \
                    as members_file, open(f'скачанные файлы/members_ids_{chat_name}.txt', 'w', encoding="utf-8") \
                    as ids_file:
                for message in self.app.get_chat_history(chat_name):
                    first_name, last_name, username, user_id, member = self.messages_data_sorting(message)
                    messages_count += 1
                    self.sock.send(str(messages_count).encode())

                    command = self.sock.recv(1024)
                    if self.pause_and_stop_handler(command) == 'stop':
                        break

                    if member not in added:
                        members_file.write(f'{members_count}. {member}')
                        ids_file.write(f'{user_id},')

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

    def messages_data_sorting(self, message):
        first_name = message.from_user.first_name if message and message.from_user and message.from_user.first_name else ' '
        last_name = message.from_user.last_name if message and message.from_user and message.from_user.last_name else ' '
        username = message.from_user.username if message and message.from_user and message.from_user.username else '.......'
        user_id = message.from_user.id if message and message.from_user and message.from_user.id else '.......'
        member = f'@{username} {first_name} {last_name} ID:{user_id}\n'
        return first_name, last_name, username, user_id, member


    def pause_and_stop_handler(self, command):
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
                    return 'stop'
        elif command.decode() == 'stop':
            return 'stop'
    def monitoring_chat(self, chat_name):
        try:
            self.sock = socket.socket()
            self.sock.connect(('localhost', 9090))
            chat_id = self.get_chat_info(chat_name=chat_name)['id']
            print(chat_id)
            self.chat_name = chat_name
            if not self.app:
                self.app = Client(name="app")

            my_handler = MessageHandler(callback=self.handler_function, filters=filters.chat(chat_id))
            self.app.add_handler(my_handler)
            if not os.path.exists('скачанные файлы'):
                os.makedirs('скачанные файлы')
            if not Path(f'скачанные файлы/members_ids_{chat_name}.txt').is_file():
                open(f'скачанные файлы/members_ids_{chat_name}.txt', 'a').close()
            with open(f'скачанные файлы/members_ids_{chat_name}.txt', 'r') as file:
                data = file.read()

                if data:
                    self.already_added = data.split(',')

            print(f' conn is {self.app}')
            self.app.run()

        except Exception as err:
            print(err)

    async def handler_function(self, client, message):

        self.monitoring_messages_count += 1
        self.sock.send(str(self.monitoring_messages_count).encode())
        first_name, last_name, username, user_id, member = self.messages_data_sorting(message)
        print(user_id, self.already_added)
        if str(user_id) not in self.already_added:
            self.sock.send(f'Добавлен участник {member}'.encode())
            self.download_members_to_files(members_count='monitoring. ', member=member,
                                           chat_name=self.chat_name, user_id=user_id)
            self.already_added.append(str(user_id))

    def download_members_to_files(self, members_count, member, chat_name, user_id):
        if not os.path.exists('скачанные файлы'):
            os.makedirs('скачанные файлы')
        with open(f'скачанные файлы/members_{chat_name}.txt', 'a', encoding="utf-8") as file:
            file.write(f'{members_count}. {member}')
        with open(f'скачанные файлы/members_ids_{chat_name}.txt', 'a', encoding="utf-8") as file:
            file.write(f'{user_id},')

