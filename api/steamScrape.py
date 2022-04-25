import json

import requests
import whoosh
from whoosh import qparser
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.qparser import QueryParser


class gameSearchEngine(object):

    def __init__(self, ix_dir="gameIndex") -> None:
        self.index = self.init_index(ix_dir)
        self.n = 10
        self.junction_type = qparser.OrGroup
        self.search_fields = ["title", "short_desc", "about_the_game"]

    def init_index(self, ix_dir):  # Initializes the index, using optional parameters if provided
        if whoosh.index.exists_in(ix_dir):
            return open_dir(ix_dir)

        schema = Schema(app_id=ID(stored=True, unique=True, sortable=True),
                        title=TEXT(stored=True, sortable=True),
                        short_desc=TEXT(stored=True),
                        about_the_game=TEXT(stored=True),
                        achievements=NUMERIC(stored=True, sortable=True),
                        full_price=NUMERIC(stored=True, sortable=True),
                        discount_price=NUMERIC(stored=True, sortable=True),
                        discount_percent=NUMERIC(stored=True, sortable=True),
                        platforms=KEYWORD(stored=True, commas=True, lowercase=True),
                        genres=KEYWORD(stored=True, commas=True, lowercase=True),
                        developers=KEYWORD(stored=True, commas=True, lowercase=True),
                        publishers=KEYWORD(stored=True, commas=True, lowercase=True),
                        image_url=TEXT(stored=True),
                        total_reviews=NUMERIC(stored=True, sortable=True),
                        release_date=TEXT(stored=True))

        return create_in(ix_dir, schema)

    def swap_junction_type(self):  # Swaps the query junction type between OR or AND
        if self.junction_type == qparser.OrGroup:
            self.junction_type = qparser.AndGroup  # Simple swap between the two types
        else:
            self.junction_type = qparser.OrGroup.factory(0.8)

    def linearize_list(self, list):  # Return a list in string format for indexing
        string = ""
        if len(list) != 0:
            for element in list:  # For each element in the list
                string += element.replace(",", "")  # separate  them with a comma
                if len(list) - 1 == list.index(element):
                    break
                string += ","

        return str(string)

    def add_index_doc(self, data):  # Takes in a list of dictionaries and returns the index over the data

        writer = self.index.writer()

        writer.add_document(app_id=str(data[12]),
                            title=data[0],
                            short_desc=data[1],
                            about_the_game=data[2],
                            achievements=str(data[3]),
                            full_price=str(data[4]),
                            discount_price=str(data[5]),
                            discount_percent=str(data[6]),
                            platforms=self.linearize_list(data[13]),
                            genres=self.linearize_list(data[7]),
                            developers=self.linearize_list(data[8]),
                            publishers=self.linearize_list(data[9]),
                            image_url=data[10],
                            total_reviews=data[11],
                            release_date=data[14])

        writer.commit()

    def print_topN_results(self, results, years, total_results, ids):  # Prints the results to n elements
        print()
        if len(results) == 0:
            print("No results found... :(\n")  # Results is empty
            return
        return_count = 0
        for i in range(self.n):  # Try to print n elements from results
            return_count += 1
            print(results[i] + " - (" + years[i] + ")" + " id: " + ids[i])
            if results.index(results[i]) == len(results) - 1:  # If there arent enough elements then break
                break
        print("\nFound %d results, returned %d\n" % (total_results, return_count))  # print total vs returned results

    def all_docs(self):
        alld = self.index.searcher().documents()        # Returns all ids in the index

        ids = []
        for x in alld:
            ids.append(x['app_id'])

        return ids

    def get_max_id(self):                           # Gets the largest app_id in the index (useful for knowing where to start scraping)

        alld = self.index.searcher().documents()
        max = 0
        total = 0
        for x in alld:
            if int(max) < int(x['app_id']):     # swap if the is larger than the last
                max = x['app_id']
            total += 1

        return max

    def get_unique_attr(self, attr_name):       # Returns all unique values for the given attribute in keyword fields

        alld = self.index.searcher().documents()
        uniques = []
        for x in alld:
            att_list = x[attr_name].split(",")
            for y in att_list:
                if y not in uniques:
                    uniques.append(y)

        return uniques

    def get_by_id(self, id): # Returns all data for a given steam id / assumes id is in index

        ret = None
        with self.index.searcher() as s:
            qp = QueryParser("app_id", schema=self.index.schema) # Find the tuple
            q = qp.parse(id)
            results = s.search(q)
            ret = {"data": [dict(hit) for hit in results]}      # Put tuple in a dict
        return ret

    def date_sorter_reverse(self, searcher, docnum):  # Custom sorter for the release date format
        date = searcher.stored_fields(docnum)['release_date']
        try:
            str_date = date.replace(",", "").split(" ")

            if str_date[0] == 'Jan' : str_date[0] = "1"
            elif str_date[0] == 'Feb' : str_date[0] = "2"
            elif str_date[0] == 'Mar' : str_date[0] = "3"
            elif str_date[0] == 'Apr' : str_date[0] = "4"
            elif str_date[0] == 'May' : str_date[0] = "5"
            elif str_date[0] == 'Jun' : str_date[0] = "6"
            elif str_date[0] == 'Jul' : str_date[0] = "7"
            elif str_date[0] == 'Aug' : str_date[0] = "8"
            elif str_date[0] == 'Oct' : str_date[0] = "9"
            elif str_date[0] == 'Sep' : str_date[0] = "10"
            elif str_date[0] == 'Nov' : str_date[0] = "11"
            elif str_date[0] == 'Dec' : str_date[0] = "12"
            if len(str_date[1]) == 1: str_date[1] = "0" + str_date[1] # Pad the day
            if len(str_date[0]) == 1: str_date[0] = "0" + str_date[0] # Pad the month
            num = str_date[2]+str_date[0]+str_date[1]
            return int(num)
        except:
            return 100000000                                # Weight TBA dates highest for reverse

    def date_sorter(self, searcher, docnum):  # Custom sorter for the release date format
        date = searcher.stored_fields(docnum)['release_date']
        try:
            str_date = date.replace(",", "").split(" ")
            if str_date[0] == 'Jan':
                str_date[0] = "1"
            elif str_date[0] == 'Feb':
                str_date[0] = "2"
            elif str_date[0] == 'Mar':
                str_date[0] = "3"
            elif str_date[0] == 'Apr':
                str_date[0] = "4"
            elif str_date[0] == 'May':
                str_date[0] = "5"
            elif str_date[0] == 'Jun':
                str_date[0] = "6"
            elif str_date[0] == 'Jul':
                str_date[0] = "7"
            elif str_date[0] == 'Aug':
                str_date[0] = "8"
            elif str_date[0] == 'Oct':
                str_date[0] = "9"
            elif str_date[0] == 'Sep':
                str_date[0] = "10"
            elif str_date[0] == 'Nov':
                str_date[0] = "11"
            elif str_date[0] == 'Dec':
                str_date[0] = "12"
            if len(str_date[1]) == 1: str_date[1] = "0" + str_date[1]
            if len(str_date[0]) == 1: str_date[0] = "0" + str_date[0]
            num = str_date[2] + str_date[0] + str_date[1]
            return int(num)
        except:
            return 1            # Weight the TBA dates low for dsc

    def query_parser(self):
        return MultifieldParser(self.search_fields, schema=self.index.schema, group=self.junction_type)


class steamScraper(object):


    # Must be initialized with the steam web scraping key and last id if you have already scraped
    def __init__(self, steam_web_key, last_app_id = "0") -> None:

        self.last_id = last_app_id
        self.ids_link = "https://api.steampowered.com/IStoreService/GetAppList/v1/?&key=%s&max_results=1000&last_appid=" % steam_web_key
        self.app_request_link = "https://store.steampowered.com/api/appdetails?appids="

    def get_id_data(self, id):          # Returns data for an individual steam_id

        try:
            pg = self.get_page(self.app_request_link + str(id))
            pg = json.loads(pg.text)[str(id)]['data']
        except:
            print("ERROR code with id: " + str(id) + " | " + str(pg))
            return None
        # GAME TITLE
        try:
            title = pg['name']
        except:
            title = ""
        # GAME SHORT DESCRITPION
        try:
            short_desc = pg['short_description']
        except:
            short_desc = ""
        # ABOUT_THE GAME
        try:
            about_the_game = pg['about_the_game']
        except:
            about_the_game = ""
        # ACHIEVEMENTS
        try:
            total_achievements = pg['achievements']['total']
        except:
            total_achievements = 0
        # GAME PRICE
        try:
            if pg['is_free'] == "true":
                full_price = "0"
                discount_price = "0"
                discount_percent = "0"
            else:
                full_price = pg['price_overview']['initial']
                discount_price = pg['price_overview']['final']
                discount_percent = pg['price_overview']['discount_percent']
        except:
            full_price = "-1"
            discount_price = "-1"
            discount_percent = "-1"
        # GENRE TAGS
        genres = []
        try:
            for key in pg['genres']:
                genres.append(key['description'])
        except:
            pass
        # DEVELOPERS
        developers = []
        try:
            for key in pg['developers']:
                developers.append(key)
        except:
            pass
        # PUBLISHERS
        publishers = []
        try:
            for key in pg['publishers']:
                publishers.append(key)
        except:
            pass
        # HEADER IMAGE
        try:
            image = pg['header_image']
        except:
            image = "None"
        # TOTAL REVIEWS
        try:
            reviews = pg['recomendations']
        except:
            reviews = 0
        # STEAM APPID
        app_id = id
        # PLATFORMS
        platforms = []
        try:
            if pg['platforms']['windows'] == "true": platforms.append("windows")
            if pg['platforms']['mac'] == "true": platforms.append("mac")
            if pg['platforms']['linux'] == "true": platforms.append("linux")
        except:
            pass
        # RELEASE DATE
        try:
            if pg['release_date']['coming_soon'] == "true":
                release_date = "Coming Soon"
            else:
                release_date = pg['release_date']['date']
        except:
            release_date = "Unknown"

        print(title + " - " + str(app_id))
        return [title, short_desc, about_the_game, total_achievements, full_price,
                discount_price, discount_percent, genres, developers, publishers,
                image, reviews, app_id, platforms, release_date]

    def get_ids(self):                                  # Retrieves a list of ids starting at the last_id value

        pg = self.get_page(self.ids_link + self.last_id)
        if pg.status_code == 400:
            print("Received 400 response")              # Steam bein a bitch
            quit()
        pg = json.loads(pg.text)['response']['apps']    # Load the ids
        app_list = []
        for app in pg:
            app_list.append(app['appid'])           # List all of the ids
        return app_list

    def get_page(self, url):
        page = requests.get(url)
        return page


if __name__ == "__main__":

    # Exampel of scraping
    # key = "" # Steam key
    # scraper = steamScraper(key, "726500")
    # x = scraper.get_ids()
    # idx = gameSearchEngine()
    # for id in x:
    #     id_data = scraper.get_id_data(id)

    #     if id_data == None:
    #         time.sleep(2)
    #         continue
    #     idx.add_index_doc(id_data)
    #     time.sleep(2)

    # Example of seraching the index
    idx = gameSearchEngine()

    with idx.index.searcher() as s:

        qp = qparser.QueryParser("about_the_game", idx.index.schema)
        q = qp.parse("action")
        reverse = False

        facet = "title"

        r = s.search(q, sortedby=facet, reverse=reverse, limit=15)

        for hit in r:
            print(hit['title'] + " || " + hit['release_date'])
    # # r= idx.search("madeline platform pixel strawberry platformer precise tight")

    # # r = idx.get_by_id("575170")
    # # print(r['data'][0]['full_price'])
    # # print(r)
    # r = idx.all_docs() # prints the number of docs in the index
# r = idx.get_max_id()
# print(len(r))
