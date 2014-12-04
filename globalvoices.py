import os
import json
import feedparser
import urllib
from urllib2 import urlopen
import HTMLParser
import sqlite3

#------Database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS country
             (title text, link text, author text, content text)''')

# Insert a new row of data
c.execute("INSERT INTO country VALUES ('Andorra','http://visitandorra.com/es/home/','Judith Amores','asdas')")

# figure out what dir we are in (needed to load other files when deploying to a server)
basedir = os.path.dirname(os.path.abspath(__file__))

# read in mapping of country names to paths to RSS feeds on the Global Voices server
f = open(basedir+'/globalvoices-countrypaths.json', 'r')
path_lookup = json.loads(f.read())


def recent_stories_from(country , repeatStory):
    '''
    Return a list of the last 3 stories for a given country
    '''
    h = HTMLParser.HTMLParser()
    raw_content = urlopen( _content_url_via_google_for( country , repeatStory) ).read()
    content = json.loads( raw_content )
    stories = []

    for details in content['responseData']['feed']['entries']:
        stories.append( {
            'title': details['title'],
            'link': details['link'],
            'author': details['author'],
            'contentSnippet': h.unescape(details['contentSnippet'])
            } )
        # Insert a row of the values
        #c.execute("INSERT INTO country_table VALUES ('title','link','author','contentSnippet'")
        # Save (commit) the changes
        #conn.commit()

    return stories

def country_list():
    '''
    Return a list of all the countries with feeds on the Global Voices site
    '''
    return path_lookup.keys()

def _content_url_via_google_for(country , repeatStory):
    '''
    Return the URL to the RSS content for a country via the Google API, so we can get in JSON directly 
    (rather than in XML)
    '''
    return "http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num="+str(repeatStory)+"&q="+ urllib.quote( _rss_url_for(country).encode("utf-8") )

def _rss_url_for(country):
    '''
    Return the URL to the RSS feed of stories for a country
    '''
    return "http://globalvoicesonline.org" + path_lookup[country] + "feed";

# Save (commit) the changes
conn.commit()
conn.close()
