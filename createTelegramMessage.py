import csv
import re
from itertools import islice
import constant
import telegram
from time import sleep
import os

bot = telegram.Bot(constant.telegramToken)

async def createTelegramMessage():
    with open('ReplaceLink.csv', 'r', encoding='UTF8') as linksFile:
        file = csv.reader(linksFile)
        for line in islice(file, 1, None):
            try:
                sleep(3)
                title = line[0]
                price = line[1]
                firstPrice = line[2]
                image = line[4]
                star = line[5]
                affiliateLink = line[6]

                if firstPrice.__len__() > 1:
                    template = f"{title}  \n \n 🤑 SUPER SCONTO \n ⭐ ️{star + ' / 5'} \n  💣 SOLO {price + '€'} \n ❌ Invece di {firstPrice + '€'}\n "
                elif price.__len__() == 0:
                    template = f"{title}  \n \n😍🌋🚀 IDEA DEL GIORNO 🌌🍀🏆 \n ⭐️ {star + ' / 5'} \n 💣 {'Scopri il prezzo sul sito'} \n "
                else:
                    template = f"{title}  \n \n😍🌋🚀 IDEA DEL GIORNO 🌌🍀🏆 \n ⭐️ {star + ' / 5'} \n 💣 {price + '€'} \n "

                button_1 = telegram.InlineKeyboardButton(text='📩Invita un amico', url=constant.channelLink)
                button_2 = telegram.InlineKeyboardButton(text="📱Vai al sito", url=f'{affiliateLink}')
                keyboard_inline = telegram.InlineKeyboardMarkup([[button_1, button_2]])
                await bot.send_message(text=f"[\n]({image}) \n{template}", parse_mode='markdown', chat_id=constant.channel_id, reply_markup=keyboard_inline)
            except Exception as e:
                if e.__str__().__contains__('entity'):
                    pass
                else:
                    raise e


def replaceAffiliateLink():
    header = ['Title', 'Price', 'FirstPrice', 'Link', 'Image', 'Star', 'ReplaceLink']
    with open('ReplaceLink.csv', 'w', encoding='UTF8', newline='') as fileReplacedLinks:
        writer = csv.writer(fileReplacedLinks)
        writer.writerow(header)
        with open('AmazonWebScraperDataset.csv', 'r',  encoding='UTF8', newline='') as file:
         lines = csv.reader(file)
         for line in islice(lines, 1, None):
            try:
                title = line[0]
                price = line[1]
                firstPrice = line[2]
                link = line[3]
                image = line[4]
                star = line[5]
                dpPosition = link.find('dp')
                productCode = re.search(r'(?:dp\/[\w]*)|(?:gp\/product\/[\w]*)', link[dpPosition:].split(" ")[0])
                finalLink = constant.baseURL + productCode.group(0).__str__() + constant.URLaffiliateelement + constant.affiliateCode + constant.URLfinalelement
                data = [title, price, firstPrice, link, image, star, finalLink]
                writer.writerow(data)
            except Exception as e:
               raise e



def resetCsv():
    os.remove('AmazonWebScraperDataset.csv')
    os.remove('ReplaceLink.csv')




    

