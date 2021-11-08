from logging import debug
import requests
import http
import json
from flask import Flask, render_template, request, jsonify
from newspaper import *

outlets = {
    "Yahoo": "yahoo.com/",
    "Axios": "axios.com/",
    "Bloomberg": "bloomberg.com/",
    "The New York Times": "nytimes.com/",
    "The Guardian": "theguardian.com/",
    "Business Insider": "businessinsider.com/",
    "The Washington Post": "washingtonpost.com/",
    "The New Yorker": "newyorker.com/",
    "The Atlantic": "theatlantic.com/",
    "The Washington Times": "washingtontimes.com/",
    "The Wall Street Journal": "wsj.com/",
    "CNBC": "cnbc.com/",
    "CNN": "cnn.com/",
    "FOX": "foxnews.com/",
    "Barron's": "barrons.com/",
    "Insider": "insider.com/",
    "Crain's New York": "crain.com/",
    "Fast Company": "fastcompany.com/",
    "Entrepreneur": "entrepreneur.com/",
    "Forbes": "forbes.com/",
    "Fortune": "fortune.com/",
    "Inc." : "inc.com/",
    "MarketWatch": "marketwatch.com/",
    "Money.com": "money.com/",
    "TechCrunch": "techcrunch.com/",
    "Protocol": "protocol.com/",
    "The Information": "theinformation.com/",
    "CNet": "cnet.com/",
    "HousingWire": "housingwire.com/",
    "Inman": "inman.com/",
    "National Mortgage News": "nationalmortgagenews.com/",
    "Scotsman Guide": "scotsmanguide.com/",
    "USA Today": "usatoday.com/",
    "Quartz": "quartz.com/",
    "Real Simple": "realsimple.com/",
    "Vox": "vox.com/"
}
headers = {
    'Authorization': 'Bearer 244ff6660552870e5e427bdc2e34cb7e795ed249',
    'Content-Type': 'application/json',
}

def links(file):
    with open(file, "r") as f: 
        urls = f.read().splitlines()
    return urls

def shorten(url):
    data = '{ "long_url": "' + url + '"}'
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    return response.json()['id']

def analyze(url):
    article = Article(url.strip())
    article.download()
    article.parse()
    return article

def source(url):
    outlet = ""
    for out, dmn in outlets.items():
        if dmn in url: outlet = out
    if (outlet == ""): outlet = url.split(".")[1].capitalize()
    return outlet
        
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        content = request.form.get('content')
        print(content)
        return jsonify({"content": main(content)})
    return render_template('index.html')


def main(links):
    print(links)
    urls = links.splitlines()
    print(urls)
    new = []

    for url in urls:
        print("pass=================================================")
        print(url)
        print(url.strip())
        url = url.strip()
        bitly  = shorten(url)
        outlet = source(url)
        try:
            title = analyze(url.strip()).title
        except: 
            title = "[failed to fetch title]"
        print(title)

        new.append((outlet+": "+ title+ " https://"+bitly))
        print(new)

    return new

#main()
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)