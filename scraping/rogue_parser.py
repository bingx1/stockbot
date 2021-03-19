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
        item_dict = {}
        entries = soup.find_all(class_='rhpa-opts option grouped-rhpa')
        for entry in entries:
            # print(entry)
            item_dict['name'] = entry.find(class_='simple-name').contents[0]
            item_dict['stock'] = not entry.find(class_='simple is-oos')
            item_dict['price'] = extract_price(entry.find(class_='simple-price condensed').contents[0])
            item_dict['img_url'] = get_thumbnail(soup)
            break
        if soup.find(class_='configuration'):
            item_dict['config']  = self.handle_configuration(soup)

        return item_dict
    
    def handle_configuration(self, soup):
        configuration = soup.find(class_='configuration')
        config = {}
        # attributes
        attributes = configuration.find_all(class_='attribute')
        for attribute in attributes:
            swatches = attribute.find_all(class_='swatch-holder')
            for swatch in swatches:
                if swatch.find(class_ = 'swatch active bin'):
                    config[swatch.find(class_ = 'swatch active bin')['data-value']] = False
                elif swatch.find(class_ = 'swatch active'):
                    config[swatch.find(class_ = 'swatch active')['data-value']] = True
                elif swatch.find(class_ = 'swatch bin'):
                    config[swatch.find(class_='swatch bin')['data-value']] = False
                elif swatch.find(class_='swatch'):
                    config[swatch.find(class_='swatch')['data-value']] = True
        return config
        
    def parse_single_item(self, soup):
        in_stock = False
        if soup.find(class_="button btn-size-m red full"):
            in_stock = True
        price = extract_price(soup.find(class_="main-price").contents[0])
        name = soup.find(class_='name').contents[0]
        thumbnail = get_thumbnail(soup)
        result = {'name': name, 'price': price,
                  'stock': in_stock, 'img_url': thumbnail}
        return result

    def parse_plates(self, soup):
        plates = soup.find_all(class_='swatch-holder')
        item = {}
        item['name'] = soup.find(class_='name').contents[0]
        config = {}
        stock = False
        for swatch in plates:
            if swatch.find(class_ = 'swatch active bin') or swatch.find(class_ = 'swatch bin'):
                config[swatch.find('span').text] = False
            elif swatch.find(class_ = 'swatch active') or swatch.find(class_='swatch'):
                config[swatch.find('span').text] = True
                stock = True
        item['stock'] = stock
        item['price'] = None
        item['config'] = config
        return item

def extract_price(price_string: str) -> int:
    """Helper function to convert a string in the form 'A$1,595.00' to an integer 1595"""
    return int(price_string.split('.')[0].replace(',', '')[2:])


def get_thumbnail(soup: BeautifulSoup): 
    '''Helper function to retrieve the url location of the items thumbnail from html'''
    if soup.find(class_='hero main-container-fluid'):
        # Images are loaded by JS - CANT RETRIEVE
        return None
    else:
        return soup.find(class_="image aspect-169 active i-c").findChild("img")['src']







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