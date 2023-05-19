import os
import random
from bs4 import BeautifulSoup
import requests
import csv


def scrapingProducts(URL):

    UA_STRINGS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 \
            (KHTML, like Gecko)Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36 \
            (KHTML,likeGecko)Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh;Intel Mac OS X 10_15_7)AppleWebKit/537.36 \
            (KHTML, like Gecko)Chrome/109.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 \
            (KHTML, like Gecko)Chrome/81.0.4044.138 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64)AppleWebKit/537.36 \
            (KHTML, like Gecko)Chrome/110.0.0.0 Safari/537.36"

    ]

    headers = {
        "User-Agent": random.choice(UA_STRINGS),
        'Accept-Language':'en-US,en;q=0.5'
    }

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")

    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    header = ['Title', 'Price', 'FirstPrice', 'Link', 'Image', 'Star', 'ReplaceLink']

    with open('AmazonWebScraperDataset.csv', 'a+',  encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        if os.stat('AmazonWebScraperDataset.csv').st_size == 0:
            writer.writerow(header)

        elements = soup2.findAll('div', class_='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')

        for element in elements:
            title = element.find('span', class_='a-size-base-plus a-color-base a-text-normal')
            link = element.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').get('href')
            price = element.find('span', class_='a-price-whole')
            firstPrice = element.find('span', class_='a-price a-text-price')
            image = element.find('img').get('src')
            star = element.find('span', class_='a-size-base')


            titleItem = title.text.strip()
            linkItem = link
            imageItem = image

            if price != None:
                priceItem = price.text.strip()
            else:
                priceItem = ''

            if firstPrice != None:
                firstPriceItem = firstPrice.text.strip()[:20].split(' ')[0]
            else:
                firstPriceItem = ''

            if star != None:
                starItem = star.text.strip()
            else:
                starItem = ''


            if (titleItem.__len__() > 1):
             data = [titleItem, priceItem, firstPriceItem, linkItem, imageItem, starItem]
             writer.writerow(data)
