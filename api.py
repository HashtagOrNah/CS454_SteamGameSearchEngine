from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/api/')
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/api/search')
def search():
    params = request.args.to_dict()
    print(params["q"])
    resp = dict()
    results = list()
    for i in range(10):
        results.append({
            "id": i,
            "img": "https://cdn.akamai.steamstatic.com/steam/apps/218620/header.jpg?t=1646834144",
            "title": "Payday 2",
            "desc": "PAYDAY 2 is an action-packed, four-player co-op shooter that once again lets gamers don the masks of the original PAYDAY crew - Dallas, Hoxton, Wolf and Chains - as they descend on Washington DC for an epic crime spree."
        })
    resp["results"] = results
    return resp
