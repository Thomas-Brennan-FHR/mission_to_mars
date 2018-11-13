from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from mission_to_mars import scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    result = mongo.db.mars.find_one()
    return render_template("index.html", result=result)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars
    scraped_data = scrape()
    mars_data.update({},scraped_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
