from pyrogram import Client, filters
from datetime import datetime
from logger import printl
from sql import SQL
import time
from secret_utils import *

cfg = read_cfg("string_session")

app = Client(name="grab", session_string=cfg[0], api_id=cfg[1], api_hash=cfg[2])

bd = SQL("channeldb", "channeldb", read_pswd("db_password"))


@app.on_message(filters.chat(bd.get_donor()))
def get_post(client, message):
    username = message.chat.username
    message_id = message.id

    if not bd.message_id_exists(username, message_id):
        bd.add_message_id(username, message_id)
        # перессылка поста на модеркe
        message.forward(bd.get_moder())
        client.send_message(bd.get_moder(), bd.get_last_rowid()[0])


@app.on_message(filters.chat(int(bd.get_moder())))
def send_post(client, message):
    # получаем запись в таблице
    username = bd.get_data_in_table(message)[1]
    msg_id = int(bd.get_data_in_table(message)[2])
    printl(str(bd.get_data_in_table(message)))
    printl(str(username))
    printl(str(bd.get_channel()))
    send = app.get_messages(username, msg_id)
    # send.forward(bd.get_channel(), as_copy=True)
    send.copy(str(bd.get_channel()))


if __name__ == '__main__':
    print(datetime.today().strftime(f'%H:%M:%S | Bot Telegram-Grabber launched.'))
    app.run()

