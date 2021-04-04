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
