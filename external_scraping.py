# Scraping Gamers Gate, Humble Bundle, GOG, Epic, 
from steamScrape import gameSearchEngine
import requests, json, re
from bs4 import BeautifulSoup
from selenium import webdriver

class PriceFetcher(object):

    def get_all_prices(self, game_name):

        prices = []
        try:
            h_price = self.get_humble_price(game_name)
            prices.append({"site": "Humble Bundle", "price": h_price})
        except:
            pass
            
        return prices

    def get_epic_price(self, title):

        endpoint = "https://graphql.epicgames.com/graphql"

        query = {
            "query": "\n        query catalogQuery(\n            $productNamespace:String!,\n            $offerId:String!,\n            $locale:String,\n            $country:String!,\n            $lineOffers: [LineOfferReq]!) {\n                Catalog {\n                    catalogOffer(namespace: $productNamespace,\n                        id: $offerId,\n                        locale: $locale) {\n                            namespace\n                            effectiveDate\n                            id\n                            customAttributes {\n                                key\n                                value\n                            }\n                            items {\n                                id\n                                status\n                                customAttributes {\n                                    key\n                                    value\n                                }\n                            }\n                    }\n                }\n                PriceEngine {\n                    price(country: $country, lineOffers: $lineOffers) {\n                        totalPrice {\n                            discountPrice\n                            originalPrice\n                            voucherDiscount\n                            discount\n                            currencyCode\n                            currencyInfo {\n                                decimals\n                            }\n                            fmtPrice(locale: $locale) {\n                                originalPrice\n                                discountPrice\n                                intermediatePrice\n                            }\n                        }\n                        lineOffers {\n                            appliedRules {\n                                endDate\n                                discountSetting {\n                                    discountType\n                                }\n                            }\n                        }\n                    }\n                }\n            }\n        ",
            "variables": {
                "productNamespace": "cosmos",
                "offerId": "1c55202badfc4212b4f82553d5d22c3e", # This is found in the first request we made,
                "locale": "en-US",                             # data.Storefront.storefrontModules[1].offers[""0""].id to be more precise.
                "country": "US",
                "lineOffers": [{
                    "offerId": "1c55202badfc4212b4f82553d5d22c3e", # The same id goes here too.
                    "quantity": 1
                }],
                "calculateTax": False}
            }

        data = requests.post(endpoint, headers={"Content-type": "application/json;charset=UTF-8"
                                            }, data=json.dumps(query)) # We added json.dumps because it basically turns dictionary
                                                                        # into JSON string.
        print(data.json()["data"]["PriceEngine"])

    def get_humble_price(self, title):

        #url = "https://www.humblebundle.com/store/api/search?request=1&search=" Couldnt get this to work
        url = "https://www.humblebundle.com/store/"

        title = title.split('/')[0]
        title = title.lower()
        title = title.replace("'", "")
        title = re.sub("[^0-9a-zA-Z]+", "-", title)
        new_string = ""
        while title != new_string:
            #print(title)
            new_string = title
            title = title.replace("--", "-")
        if title[-1] == "-":
            title = title[0:-1]
        print(title)

        url = url + title
        #url = "https://www.humblebundle.com/store/beamngdrive"
        page = requests.get(url)
        data = BeautifulSoup(page.content, 'html.parser')

        price_str = data.find_all('script')
        price = json.loads(price_str[2].text)["offers"]['price']
        
        return price


if __name__=="__main__":

    # idx = gameSearchEngine()
    # r = idx.get_by_id("504230")
    # print(r["data"][0]['title'])
    x = PriceFetcher()
    name = "awf"
    #name = "Middle-earth™: Shadow of War™ Definitive Edition"
    x.get_humble_price(name)
