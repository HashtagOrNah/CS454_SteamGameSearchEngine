from flask import Flask
from flask import request
from steamScrape import gameSearchEngine
app = Flask(__name__)

@app.route('/api/')
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/api/search')
def search():
    searcher = gameSearchEngine()
    params = request.args.to_dict()
    print(params["q"])
    query = params["q"]
    results = searcher.search(query)
    resp = dict()
    resp["results"] = results[:10]
    return resp
