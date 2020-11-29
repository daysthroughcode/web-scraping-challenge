from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

# render index.html using previous data
@app.route("/")
def index():

    # Find Record of data in mongodb db
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)


# Trigger Route For Scrape Function
@app.route("/scrape")
def scrape():

    # Run scrape fn
    mars_data = scrape_mars.scrape()

    # Update Mongo database 
    mongo.db.mars_data.update({}, mars_data, upsert=True)
    return 'Complete!'

if __name__ == "__main__":
    app.run(debug=True)