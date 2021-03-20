import requests
from bs4 import BeautifulSoup

class KabukiParser():
    def __init__(self) -> None:
        self.manufacturer = 'Kabuki'

    def parse_html(self, soup):
        name = soup.find(class_='product_name').text
        price = soup.find(class_='current_price').find(class_='money').text
        stock = True
        if soup.find(class_='sold_out').text:
            stock = False
        finish = soup.find('select')
        if finish:
            finishes = finish.findChildren('option')
            for coating in finishes:
                if coating.get('selected'):
                    name = name + ' - ' + coating.text
        imgs = soup.find(class_='slides')
        img_url = imgs.find('li').find(class_='fancybox').get('href')
        img_url = 'https' + img_url
        item = {}
        item['name'] = name
        item['stock'] = stock
        item['price'] = price
        item['img_url'] = img_url
        return item
        

if __name__ == '__main__':
    KabukiParser = KabukiParser()

    req = requests.get('https://store.kabukistrength.net/collections/cosmetic-blemish/products/duffalo-bar-cosmetic-blemish?variant=44627006478')
    soup = BeautifulSoup(req.text, 'html.parser')
    item = KabukiParser.parse_html(soup)
    print(item)
    req = requests.get('https://store.kabukistrength.net/collections/cosmetic-blemish/products/duffalo-bar-cosmetic-blemish?variant=40054564238')
    soup = BeautifulSoup(req.text, 'html.parser')
    item = KabukiParser.parse_html(soup)
    print(item)
    req = requests.get('https://store.kabukistrength.net/collections/cosmetic-blemish/products/duffalo-bar-cosmetic-blemish?variant=40054600654')
    soup = BeautifulSoup(req.text, 'html.parser')
    item = KabukiParser.parse_html(soup)
    print(item)