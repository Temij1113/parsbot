# -*- coding: utf-8 -*-
import config
import telebot
import requests
import csv
import json
import datetime
import time

from poluchenie import file_maker

#Без обновления не работает
URL = "https://api.telegram.org/bot" + config.token + "/"

proxies = {
    'https': 'socks5://3.212.104.192:3128'
}

def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url, proxies=proxies, ).text
    print(r)

spis_is_id=[]


bot = telebot.TeleBot(config.token)
vr = time.strftime("%H:%M",time.localtime())


def otvet():
    FILE = 'posts.csv'
    print(1)
    #if  message.text.lower() == 'новый пост':
    with open(FILE, "r", newline="",encoding="utf-8") as file:
        with open('otp_post','r+') as fl:
            reader = csv.DictReader(file)
            b=0
            while b<4:
                for row in reader:
                        for stroka in fl.readlines():
                            if stroka != spis_is_id:
                                spis_is_id.append(stroka.strip())
                        if str(row["id"]) in spis_is_id:
                            continue
                        else:
                            fl.write(str(row["id"]+"\n"))
                            if row["type"]== 'photo':
                                bot.send_photo(-1001240055823,photo = row["url"],caption = row["text"] )

                            elif row["type"]=='video':
                                bot.send_photo(-1001240055823,photo=row["url"],caption = row["text"] )
                            print(row)
                            print(spis_is_id)
                b+=1
                if b==4:
                    break

otvet()

while True:
    time.sleep(600)
    file_maker()

if __name__ == '__main__':
    bot.polling(none_stop=True,timeout = 123)
