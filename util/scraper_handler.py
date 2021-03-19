from .rogue_parser import RogueParser
''' The scraper handler is responsible for allocating a particular parser to be used'''

class ScraperHandler():

    def __init__(self) -> None:
        self.rogue = RogueParser()
    
    def parse(self, url, soup):
        if 'rogueaustralia' in url:
            res =  self.rogue.parse_html(soup)
            res['manufacturer'] = self.rogue.manufacturer
            return res
    