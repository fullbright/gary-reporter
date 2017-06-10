from pocket import Pocket, PocketException
import json
import os
import email_notify
import logging
import logging.handlers

logger = logging.getLogger('garyreporter')
logger.setLevel(logging.DEBUG)
current_script_file = os.path.realpath(__file__)
current_script_dir = os.path.abspath(os.path.join(current_script_file, os.pardir))
fh = logging.handlers.RotatingFileHandler(
              "%s/logs/garyreporter.log" % (current_script_dir),
                            maxBytes=200000, backupCount=5)
#logging.FileHandler("%s/eepm_video_processor.log" % (current_script_dir))
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


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
    data_origin = None

    if not os.path.isfile(articles_json_data_file):
        print "Requesting articles from GetPocket ..."
        articles_json = p.retrieve(tag=tagfilter, offset=myoffset, count=mycount)

        with open(articles_json_data_file, 'w') as outfile:
            json.dump(articles_json, outfile)

        data_origin = "getpocket_api"
    else:
        print "Reading local articles from file"
        articles_json = json.loads(open(articles_json_data_file).read())
        data_origin = "localfile"

    articles_count = len(articles_json['list'])
    print("Status of request : %s. Got %s articles" % (articles_json['status'], articles_count))

    found_error = False
    for article in articles_json['list']:
        try:

            print "--- --- ---"
            art_title =  articles_json['list'][article]['resolved_title'].encode('utf-8')
            art_url = articles_json['list'][article]['resolved_url'].encode('utf-8')
            art_id = articles_json['list'][article]['resolved_id'].encode('utf-8')

            print "Found new article : >>>>> #%s - (%s)[%s]" % (art_id, art_title, art_url)
            # If processed successfully, remove the tag from it
            p.tags_remove(art_id, tagfilter)
        except KeyError as ke:
            print(ke.message)
            found_error = True

    # Notify my master
    notifier = email_notify.EmailNotification("mailgun.bright-softwares.com", "Gary Reporter", "mailgun@mailgun.bright-softwares.com", logger=logger)

    email_data = [{
        "email": "sergio@afanou.com",
        "name": "Sergio Bro",
        "subject": "Hi",
        "data" : {
            "dear": "master",
            "msg": "Hola mundo",
            "found_error": found_error,
            "articles_count": articles_count,
            "data_origin": data_origin
        }
    }]

    email_result = notifier.mailgun_emailer(email_data, "email-html_notify")
    print "The email server said: ", email_result

    # Finally remove the articles json file
    if not found_error :
        os.remove(articles_json_data_file)



except PocketException as e:
    print(e.message)

