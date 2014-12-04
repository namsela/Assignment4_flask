from flask import Flask, render_template
import json
import feedparser
import globalvoices


repeatStory = 6

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("stories.html",
        country_list_json_text=json.dumps(globalvoices.country_list())
    )

@app.route("/country/<country>")
def country(country):
    #Set the number os stories to show
    stories = globalvoices.recent_stories_from( country, repeatStory )
    return render_template("stories.html",
        country_list_json_text=json.dumps(globalvoices.country_list()),
        country_name=country,
        stories=stories
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
