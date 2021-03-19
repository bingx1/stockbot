import requests
from bs4 import BeautifulSoup
from requests.api import options

class RogueParser():

    def __init__(self) -> None:
        self.manufacturer = 'Rogue'

    def parse_html(self, soup):
        # Pass in a bs4 soup
        if soup.find(class_='rhpa-opts option grouped-rhpa'):
            output = self.parse_rack(soup)
        elif soup.find(class_='swatches-container vertical'):
            output = self.parse_plates(soup)
        else:
            output = self.parse_single_item(soup)
        return output

    def parse_rack(self, soup):
        results = []
        item =soup.find(class_='rhpa-content')
        if soup.find(class_='configuration'):
            self.handle_configuration(soup)
        else:
        # product_title = item.find(class_='title').find(class_='name').contents[0]
        # Entries
            item_data = item.find(class_='rhpa bin grouped')
            entries = item_data.find_all(class_='rhpa-opts option grouped-rhpa')
            for entry in entries:
                name = entry.find(class_='simple-name').contents[0]
                status = not entry.find(class_='simple is-oos')
                price = extract_price(entry.find(class_='simple-price condensed').contents[0])
                img_url = get_thumbnail(soup)
                item_dict = {'name': name,'stock' :status,'price':price,'img_url':img_url}
                results.append(item_dict)
                break
        return results
    
    def handle_configuration(self, soup):
        configuration = soup.find(class_='configuration')
        # attributes
        attributes = configuration.find_all(class_='attribute')
        for attribute in attributes:
            swatches = attribute.find_all(class_='swatch-holder')
            for swatch in swatches:
                if swatch.find(class_ = 'swatch active bin'):
                    print('OOS', swatch.find(class_ = 'swatch active bin')['data-value'])
                elif swatch.find(class_ = 'swatch active'):
                    print('In stock', swatch.find(class_ = 'swatch active')['data-value'])
                elif swatch.find(class_ = 'swatch bin'):
                    print('OOS', swatch.find(class_='swatch bin')['data-value'])
                elif swatch.find(class_='swatch'):
                    print('In stock', swatch.find(class_='swatch')['data-value'])
        return
        
    def parse_single_item(self, soup):
        in_stock = False
        if soup.find(class_="button btn-size-m red full"):
            in_stock = True
        price = extract_price(soup.find(class_="main-price").contents[0])
        name = soup.find(class_='name').contents[0]
        thumbnail = get_thumbnail(soup)
        result = {'name': name, 'price': price,
                  'stock': in_stock, 'img_url': thumbnail}
        return [result]

    def parse_plates(self, soup):
        plates = soup.find_all(class_='swatch-holder')
        for swatch in plates:
            if swatch.find(class_ = 'swatch active bin'):
                print('OOS', swatch.find('span').text)
            elif swatch.find(class_ = 'swatch active'):
                print('In stock', swatch.find('span').text)
            elif swatch.find(class_ = 'swatch bin'):
                print('OOS', swatch.find('span').text)
            elif swatch.find(class_='swatch'):
                print('In stock', swatch.find('span').text)
        return

def extract_price(price_string: str) -> int:
    """Helper function to convert a string in the form 'A$1,595.00' to an integer 1595"""
    return int(price_string.split('.')[0].replace(',', '')[2:])


def get_thumbnail(soup: BeautifulSoup) -> str: 
    '''Helper function to retrieve the url location of the items thumbnail from html'''
    imgs = soup.find(class_="custom-scroll product-scroll")
    return imgs.find(class_="image aspect-169 active i-c").findChild("img")['src']







# Plates
# For the active option (i.e. the default option)
# class=swatch active bin - the current option (check stock by seeing if the notify me box is there)
# For the other options:
# if class = swatch bin, the item is OSS - if class is swatch - item is in stock

# Barbells
if __name__ == '__main__':
    RogueParser = RogueParser()
    # # Test rack
    # req = requests.get('https://www.rogueaustralia.com.au/rogue-rml-490-power-rack-au')
    # soup = BeautifulSoup(req.text, 'html.parser')
    # res = RogueParser.parse_html(soup)
    # print(res)
    # Test plates
    req = requests.get('https://www.rogueaustralia.com.au/rogue-color-echo-bumper-plate-au')
    soup = BeautifulSoup(req.text, 'html.parser')
    res = RogueParser.parse_html(soup)
    print(res)

    # # Test single item
    # req = requests.get('https://www.rogueaustralia.com.au/the-ohio-bar-black-zinc-au')
    # soup = BeautifulSoup(req.text, 'html.parser')
    # res = RogueParser.parse_html(soup)
    # print(res)

    # Test barbell with config options
    req = requests.get('https://www.rogueaustralia.com.au/the-ohio-bar-cerakote-au')
    soup = BeautifulSoup(req.text, 'html.parser')
    res = RogueParser.parse_html(soup)
    print(res)

    # Test rack with config options
    req = requests.get('https://www.rogueaustralia.com.au/rogue-rml-390bt-power-rack-au')
    soup = BeautifulSoup(req.text, 'html.parser')
    res = RogueParser.parse_html(soup)
    print(res)

    # Test rack with difficult config options
    req = requests.get('https://www.rogueaustralia.com.au/rogue-rml-490-power-rack-color-3-0-au')
    soup = BeautifulSoup(req.text, 'html.parser')
    res = RogueParser.parse_html(soup)
    print(res)

    # Test rack with difficult config options
    req = requests.get('https://www.rogueaustralia.com.au/rml-690c-power-rack-3-0-au')
    soup = BeautifulSoup(req.text, 'html.parser')
    res = RogueParser.parse_html(soup)
    print(res)