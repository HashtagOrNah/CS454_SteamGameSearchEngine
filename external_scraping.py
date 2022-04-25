# Scraping Gamers Gate, Humble Bundle, GOG, Epic, 
from steamScrape import gameSearchEngine
import requests, json, re
from bs4 import BeautifulSoup

class PriceFetcher(object):

    def get_all_prices(self, game_name):

        prices = []
        no_res = "Nothing Found"
        # Humble Bundle Pricing
        try:
            price, url = self.get_humble_price(game_name)
            prices.append({"site": "Humble Bundle", "price": price, "link": url})
        except:
            url = "https://www.humblebundle.com/store/search?sort=bestselling&search=" + game_name
            prices.append({"site": "Humble Bundle", "price": no_res, "link": url})
        
        # GOG Pricing
        try:
            price, url = self.get_GOG_price(game_name)
            prices.append({"site": "GOG", "price": price, "link": url})
        except:
            url = "https://www.gog.com/en/games?order=desc:score&query=" + game_name
            prices.append({"site": "GOG", "price": no_res, "link": url})

        # Fanatical Pricing
        try:
            price, url = self.get_fanatical_price(game_name)
            prices.append({"site": "Fanatical", "price": price, "link": url})
        except:
            url = "https://www.fanatical.com/en/search?search=" + game_name
            prices.append({"site": "Fanatical", "price": no_res, "link": url})
        
        return prices

    def get_humble_price(self, title): # Scrapes the humble bundle price

        url = "https://www.humblebundle.com/store/"

        title = self.parse_title(title, "-") # Get the title parsed for HB

        url = url + title
        page = requests.get(url)
        data = BeautifulSoup(page.content, 'html.parser') # Get page

        price_str = data.find_all('script')
        price = json.loads(price_str[2].text)["offers"]['price'] # Find the price
        
        return price, url
    
    def get_GOG_price(self, title): # returns GOG pricing 

        url = "https://www.gog.com/en/game/"
        title = self.parse_title(title, "_") # Parse title for GOG
        url = url + title
        page = requests.get(url)
        data = BeautifulSoup(page.content, 'html.parser') # get page

        price_str = data.find_all('script')
        price = json.loads(price_str[0].text)["offers"]['price'] # get price

        return price, url
    
    def get_fanatical_price(self, title): # returns Fanatical pricing

        url = "https://www.fanatical.com/api/products-group/"
        game_page_url = "https://www.fanatical.com/en/game/"

        title = self.parse_title(title, "-") # parse title

        url = url + title

        page = requests.get(url)
        data = json.loads(page.content) # get page 
        price = data['currentPrice']['USD'] # get price
        price = str(round(float(price)*0.01, 2)) # format price to standard

        return price, game_page_url+title

    def parse_title(self, title, sep_char): # Parses the title to standard formating for website urls

        title = title.split('/')[0]
        title = title.lower()
        title = title.replace("'", "")
        title = re.sub("[^0-9a-zA-Z]+", sep_char, title) # strip symbol characters 
        new_string = ""
        while title != new_string:
            #print(title)
            new_string = title
            title = title.replace(2*sep_char, sep_char) # create separators
        if title[-1] == sep_char:
            title = title[0:-1]
        
        return title

if __name__=="__main__":

    x = PriceFetcher()
    name = "No Turning Back: The Pixel Art Action-Adventure Roguelike"
    #name = "Middle-earth™: Shadow of War™ Definitive Edition"
    p = x.get_all_prices(name)
    # p = x.get_fanatical_price(name)
    print(p)
