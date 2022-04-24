from ast import Str
from flask import Flask
from flask import request
from whoosh.searching import ResultsPage
from external_scraping import PriceFetcher
from steamScrape import gameSearchEngine
from whoosh import scoring
from whoosh.query import And
from whoosh.query import Term

app = Flask(__name__)
engine = gameSearchEngine()

@app.route('/api/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/search')
def search():
    global engine
    # parse request args
    params = request.args.to_dict()

    if "q" not in params or params["q"] == "":
        return "Missing Query", 400


    query = engine.query_parser().parse(params["q"])
    pagenum = 1
    try:
        pagenum = int(params["pagenum"])
    except (KeyError, ValueError):
        pass
    except Exception as e:
        print(e)
        return "Internal Server Error", 500

    # Prepare response
    resp = dict()
    resp["results"] = list()

    # prepare searcher
    with engine.index.searcher(weighting=scoring.TF_IDF) as s:

        advanced_terms = []
        if "genre" in params:
            for x in params['genre'].split(","):
                advanced_terms.append(Term("genres", x))
        if "pub" in params:
            for x in params['pub'].split(","):
                advanced_terms.append(Term("publishers", x))
        if "dev" in params:
            for x in params['dev'].split(","):
                advanced_terms.append(Term("developers", x))

        resp["result_count"] = s.search(query, scored=False).estimated_length()
    
        #rp = s.search_page(query=query, pagenum=pagenum).And(advanced_terms)
        fq = And(advanced_terms)
        r = s.search(query, filter=fq)
        rp = ResultsPage(r, pagenum)
        for x in rp:
            resp["results"].append({
                "title": x["title"],
                "id": x["app_id"],
                "img": x["image_url"],
                "desc": x["short_desc"]
            })
        resp["is_last_page"] = rp.is_last_page()

    return resp

@app.route('/api/<gid>/details')
def get_details(gid):
    global engine
    game_data = engine.get_by_id(gid)
    return game_data['data'][0]

@app.route('/api/<gid>/prices')
def price_search(gid):
    global engine
    game_data = engine.get_by_id(str(gid))
    pf = PriceFetcher()
    prices = pf.get_all_prices(game_data['data'][0]['title']) # Returns list of dicts IE {site: site_name, price: game_price, link: sites_game_link}

    return {"prices": prices}

@app.route('/api/genres')
def get_unique_genres():
    global engine
    genre_list = engine.get_unique_attr("genres")
    return {"genres": genre_list}

@app.route('/api/dev')
def get_unique_devs():
    global engine
    dev_list = engine.get_unique_attr("developers")
    return {"devs": dev_list}

@app.route('/api/pub')
def get_unique_pubs():
    global engine
    pub_list = engine.get_unique_attr("publishers")
    return {"pubs": pub_list}