from pocket import Pocket, PocketException
import json
import os

j = json.loads(open("config.json").read())

p = Pocket(
    consumer_key=j['consumer_key'],
    access_token=j['access_token']
)

# Fetch a list of articles

mycount = 100
myoffset = 0
tagfilter = "garyreporter"
articles_json_data_file = 'articles_json_data.json'

try:
    #articles_json = json.loads(p.retrieve(offset=myoffset, count=mycount))
    articles_json = None

    if not os.path.isfile(articles_json_data_file):
        print "Requesting articles from GetPocket ..."
        articles_json = p.retrieve(tag=tagfilter, offset=myoffset, count=mycount)

        with open(articles_json_data_file, 'w') as outfile:
            json.dump(articles_json, outfile)


    else:
        print "Reading local articles from file"
        articles_json = json.loads(open(articles_json_data_file).read())

    print("Status of request : %s. Got %s articles" % (articles_json['status'], len(articles_json['list'])))

    for article in articles_json['list']:
        print "--- --- ---"
        art_title =  articles_json['list'][article]['resolved_title'].encode('utf-8')
        art_url = articles_json['list'][article]['resolved_url'].encode('utf-8')
        art_id = articles_json['list'][article]['resolved_id'].encode('utf-8')

        print "Found new article : >>>>> #%s - (%s)[%s]" % (art_id, art_title, art_url)
        # If processed successfully, remove the tag from it
        p.tags_remove(art_id, tagfilter)


    # Finally remove the articles json file
    os.remove(articles_json_data_file)

except PocketException as e:
    print(e.message)

# Add an article
p.add('https://pymotw.com/3/asyncio/')

# Start a bulk operation and commit
p.archive(1186408060).favorite(1188103217).tags_add(
    1168820736, 'Python'
).tags_add(
    1168820736, 'Web Development'
).commit()
