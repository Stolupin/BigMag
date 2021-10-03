import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://hyperxpromo.com/ua/?utm_source=Twitch&utm_medium=Twitch_banner&utm_campaign=Influencers_BTS21_campaign&utm_content=Influencers_BTS21_shef_fn_b'
HEADERS =  {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Accept': '*/*'}
FILE = 'hyper.csv'
HOST = 'https://hyperxpromo.com'
def get_html(url, params = None):
    r = requests.get(url,headers = HEADERS, params=params)
    return r
cards = []
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_= 'col-6 col-sm-12 col-md-6 col-lg-3')

    for item in items:
        cards.append({
            'title': item.find('figcaption', class_='info-wrap').find('h4').get_text(),
            'price': item.find('div', class_='price-new').text.replace('\n', ''),
            'image':HOST + item.find('div', class_='img-wrap').find('img').get('src')
        })
    print(cards)

def save_file(items,path):
    with open(path,'w', newline ='') as file:
        writer = csv.writer(file,delimiter = ';')
        writer.writerow(['Модель','Цена','Ссылка фото'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['image']])
def parse():
    html = get_html(URL)
    if html.status_code ==200:
        get_content(html.text)
        save_file(cards, FILE)
    else:
        print ('Error')





parse()