from pocket import Pocket, PocketException
import json

j = json.loads(open("config.json").read())

p = Pocket(
    consumer_key=j['consumer_key'],
    access_token=j['access_token']
)

# Fetch a list of articles
try:
    print(p.retrieve(offset=0, count=10))
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
