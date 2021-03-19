import requests
from bs4 import BeautifulSoup

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
        # Title
        # title_data = item.find(class_='title')
        # product_title = title_data.find(class_='name').contents[0]
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
    
    def parse_single_item(self, soup):
        print('Single item parser not implemented yet')
        return

    def parse_plates(self, soup):
        print("Plate parser not implemented yet")
        return

def extract_price(price_string: str) -> int:
    """Helper function to convert a string in the form 'A$1,595.00' to an integer 1595"""
    return int(price_string.split('.')[0].replace(',', '')[2:])


def get_thumbnail(soup: BeautifulSoup) -> str: 
    '''Helper function to retrieve the url location of the items thumbnail from html'''
    imgs = soup.find(class_="custom-scroll product-scroll")
    return imgs.find(class_="image aspect-169 active i-c").findChild("img")['src']




# print(entries)



# Plates
# For the active option (i.e. the default option)
# class=swatch active bin - the current option (check stock by seeing if the notify me box is there)
# For the other options:
# if class = swatch bin, the item is OSS - if class is swatch - item is in stock

# Barbells
if __name__ == '__main__':
    RogueParser = RogueParser()
    # Test rack
    req = requests.get('https://www.rogueaustralia.com.au/rogue-rml-490-power-rack-au')
    soup = BeautifulSoup(req.text, 'html.parser')
    res = RogueParser.parse_html(soup)
    print(res)
    # Test plates
    req = requests.get('https://www.rogueaustralia.com.au/rogue-color-echo-bumper-plate-au')
    soup = BeautifulSoup(req.text, 'html.parser')
    res = RogueParser.parse_html(soup)
    print(res)

    # Test single item
    req = requests.get('https://www.rogueaustralia.com.au/the-ohio-bar-black-zinc-au')
    soup = BeautifulSoup(req.text, 'html.parser')
    res = RogueParser.parse_html(soup)
    print(res)