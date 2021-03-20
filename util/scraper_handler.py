from .rogue_parser import RogueParser
from .kabuki_parser import KabukiParser
''' The scraper handler is responsible for allocating a particular parser to be used'''

class ScraperHandler():

    def __init__(self) -> None:
        self.rogue = RogueParser()
        self.kabuki = KabukiParser()
    
    def parse(self, url, soup):
        if 'rogueaustralia' in url:
            res =  self.rogue.parse_html(soup)
            res['manufacturer'] = self.rogue.manufacturer
        elif 'kabuki' in url:
            res = self.kabuki.parse_html(soup)
            res['manufacturer'] = self.kabuki.manufacturer
        res['url'] = url
        return res
        
if __name__ == '__main__':
    items = []
    