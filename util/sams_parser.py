import requests
from bs4 import BeautifulSoup

class SamsParser():
    def parse_html(self, soup):
        item = {}
        item_html = soup.find(class_='col-sm-7')
        name = item_html.find(class_='sf-title').text
        properties = item_html.find(class_='list-unstyled')
        stock = not properties.find(class_='availability outofstock')
        brand = properties.find('a').text
        price = item_html.find('h2').span.text
        img_url = soup.find(class_='thumbnail').findChild('img')['src']
        item['name'] = name
        item['manufacturer'] = brand
        item['stock'] = stock
        item['price'] = self.extract_price(price)
        item['img_url'] = img_url
        return item

    def extract_price(self, price_str):
        string = price_str.replace('$', '')
        string = string.replace(',','')
        return float(string)

SamsParser = SamsParser()
urls = ['https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks/atx-prx-830-power-cage',
        'https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks/atx-competition-combo-rack',
        'https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks/atx-prx-840-power-cage',
        'https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks?product_id=1833',
        'https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks/atx-prx-820-power-cage',
        'https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks/atx-prx-810-power-cage',
        'https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks/atx-pulldown-seat',
        'https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks/atx-prx-800-lat-tower-option-125kg',
        'https://samsfitness.com.au/racks-cages-stands-smiths/atx-commercial-power-racks/atx-hrx-810',
        'https://samsfitness.com.au/dumbbells/ironmaster-quick-lock-dumbbell-system/ironmaster-quick-lock-dumbbells-base-kit',
        'https://samsfitness.com.au/ironmaster/quick-lock-dumbbell-165lb-kit',
        'https://samsfitness.com.au/ironmaster/ironmaster-quick-lock-add-on-kit',
        'https://samsfitness.com.au/barbells/elite-olympic-bars/atx-ram-power-bar']
items = []
for url in urls:
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    item = SamsParser.parse_html(soup)
    item['url'] = url
    items.append(item)
    # print(item)

print(items)