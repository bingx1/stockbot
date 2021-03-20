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
        img_url = 'https:' + img_url
        item = {}
        item['name'] = name
        item['stock'] = stock
        item['price'] = self.extract_price(price)
        item['img_url'] = img_url
        return item

    def extract_price(self, price_str):
        return float(price_str[2:])
        

