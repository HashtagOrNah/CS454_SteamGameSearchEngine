from flask import Flask
from flask import request
from whoosh.searching import ResultsPage

from steamScrape import gameSearchEngine
from whoosh import scoring

app = Flask(__name__)


@app.route('/api/')
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/api/search')
def search():
    engine = gameSearchEngine()
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
        resp["result_count"] = s.search(query, scored=False).estimated_length()

        rp = s.search_page(query=query, pagenum=pagenum)
        for x in rp:
            resp["results"].append({
                "title": x["title"],
                "id": x["app_id"],
                "img": x["image_url"],
                "desc": x["short_desc"]
            })
        resp["is_last_page"] = rp.is_last_page()

    return resp
