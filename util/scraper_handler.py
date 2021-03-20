from .rogue_parser import RogueParser
from .kabuki_parser import KabukiParser
from .sams_parser import SamsParser
''' The scraper handler is responsible for allocating a particular parser to be used'''

class ScraperHandler():

    def __init__(self) -> None:
        self.rogue = RogueParser()
        self.kabuki = KabukiParser()
        self.sams = SamsParser()

    def parse(self, url, soup):
        if 'rogueaustralia' in url:
            res = self.rogue.parse_html(soup)
        elif 'kabuki' in url:
            res = self.kabuki.parse_html(soup)
        elif 'samsfitness' in url:
            res = self.sams.parse_html(soup)
        res['url'] = url
        return res
        
if __name__ == '__main__':
    items = []
    