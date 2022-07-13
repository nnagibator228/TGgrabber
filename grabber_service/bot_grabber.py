from pyrogram import Client, filters
from datetime import datetime
from logger import printl
from sql import SQL
import time
from secret_utils import *

cfg = read_cfg("string_session")

bot = Client(name="grab", session_string=cfg[0], api_id=cfg[1], api_hash=cfg[2])

bd = SQL("channeldb", "channeldb", read_pswd("db_password"))


@bot.on_message(filters.chat(bd.get_donor()))
def get_post(client, message):
    printl("----------------------------------------------------------------------------\n")
    username = message.chat.username
    message_id = message.id
    printl(str(username) + " - " + str(message_id) + " - " + str(not bd.message_id_exists(username, message_id)) + "\n")
    printl("'"+str(bd.get_moder())+"'\n")
    if not bd.message_id_exists(username, message_id):
        printl(str(bd.add_message_id(username, message_id))+"\n")
        # перессылка поста на модеркe
        message.forward(int(bd.get_moder()))
        client.send_message(int(bd.get_moder()), bd.get_last_rowid()[0])
        printl(datetime.today().strftime(f'%H:%M:%S | Message obtained.\n'))
        printl(str(bd.get_moder())+"\n")
        printl(str(bd.get_last_rowid()[0])+"\n")


@bot.on_message(filters.chat(int(bd.get_moder())))
def send_post(client, message):
    # получаем запись в таблице
    username = bd.get_data_in_table(message)[1]
    msg_id = int(bd.get_data_in_table(message)[2])
    printl("----------------------------------------------------------------------------\n")
    printl(datetime.today().strftime(f'%H:%M:%S | Message sent.\n'))
    printl(str(bd.get_data_in_table(message))+"\n")
    printl(str(username))
    printl(str(bd.get_channel()))
    send = bot.get_messages(username, msg_id)
    # send.forward(bd.get_channel(), as_copy=True)
    send.copy(str(bd.get_channel()))


if __name__ == '__main__':
    printl("--------------------------------------------------------------------\n")
    printl(datetime.today().strftime(f'%H:%M:%S | Bot Telegram-Grabber launched.\n'))
    printl(str(bd.get_donor())+"\n")
    print(datetime.today().strftime(f'%H:%M:%S | Bot Telegram-Grabber launched.'))
    bot.run()
