from pocket import Pocket, PocketException
import simplejson

j = simplejson.loads("config.json")

p = Pocket(
    consumer_key=j['consumer_key'] #'67605-7d07d07daa10f7fb8dbe2b50',
    access_token=j['access_token'] #'15cc0e47-3178-44aa-99dd-9d27a7'
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
