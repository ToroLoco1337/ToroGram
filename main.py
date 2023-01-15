from dotenv import load_dotenv
from telethon import TelegramClient
import os
from datetime import datetime, timedelta
from telethon.tl.functions.channels import InviteToChannelRequest
import pytz
import asyncio
import colorama
from colorama import Fore, Back, Style
 
colorama.init(autoreset=True)
load_dotenv()
 
API_ID=os.environ.get("API_ID")
API_HASH=os.environ.get("API_HASH")
LOGO='''
 _____               _____                     
|_   _|             |  __ \                    
  | | ___  _ __ ___ | |  \/_ __ __ _ _ __ ___  
  | |/ _ \| '__/ _ \| | __| '__/ _` | '_ ` _ \ 
  | | (_) | | | (_) | |_\ \ | | (_| | | | | | |
  \_/\___/|_|  \___/ \____/_|  \__,_|_| |_| |_|
 
'''
 
utc=pytz.timezone('utc')
 
now = datetime.now(utc)
 
time_range = timedelta(days=7)
 
bot=TelegramClient("anon", API_ID, API_HASH)
 
async def message(chat):
    print(Fore.GREEN + "Message you want to send: ")
    message=input("")
    members=await bot.get_participants(chat)
    for member in members:
        try:
            if member.status.was_online<now-time_range:
                members.remove(member)
        except:
            pass
    for member in members:
        try:
            await bot.send_message(member, message)
            print(Fore.GREEN + f'Message sent to {member.username}')
            await asyncio.sleep(60)
        except:
            pass
    print(Fore.GREEN+f'Message sent to {len(members)} accounts.')
 
async def add(chat, link_add):
    my_chat=await bot.get_entity(link_add)
    members=await bot.get_participants(chat)
    for member in members:
        try:
            if member.status.was_online<now-time_range:
                members.remove(member)
        except:
            pass
    for member in members:
        try:
            await bot(InviteToChannelRequest(my_chat,[member]))
            print(Fore.GREEN + f'Added {member.username} to your group.')
            await asyncio.sleep(45)
        except:
            pass
    print(Fore.GREEN+f'Added {len(members)} accounts.')
 
async def main():
    print(Fore.GREEN + LOGO)
    print(Fore.GREEN + "[0] => Choose between your groups \n[1] => Input a group's link ")
    choice=input("")
    if choice=="0":
        chats=await bot.get_dialogs()
        public=[]
        for chat in chats:
            try:
                if chat.entity.megagroup:
                    public.append(chat)
            except:
                pass
        for i, chat in enumerate(public):
            print(Fore.GREEN + f'{chat.name} => {i}')
        print(Fore.GREEN+"Group's number: ")
        choice2=input("")
        chat=public[int(choice2)]
        print(Fore.GREEN + "[0] Send messages\n[1] Add members to your group")
        choice3=input("")
        if choice3=="0":
            await message(chat)
        elif choice3=="1":
            print(Fore.GREEN + "Your group's link: ")
            link_add=input("")
            await add(chat, link_add)
    elif choice=="1":
        print(Fore.GREEN + "Group's link: ")
        link=input("")
        chat=await bot.get_entity(link)
        choice4=input("")
        if choice4=="0":
            await message(chat)
        elif choice4=="1":
            print(Fore.GREEN + "Your group's link: ")
            link_add=input("")
            await add(chat, link_add)
 
with bot:
    bot.loop.run_until_complete(main())