import os, json, urllib.request
from xml.sax.saxutils import escape
from email.utils import formatdate

TOKEN = os.environ["TMDB_TOKEN"]
URL = "https://api.themoviedb.org/3/movie/now_playing?language=fr-FR&region=FR&page=1"
IMG = "https://image.tmdb.org/t/p/w500"

req = urllib.request.Request(URL, headers={"Authorization": "Bearer " + TOKEN, "accept": "application/json"})
with urllib.request.urlopen(req, timeout=30) as r:
    films = json.load(r)["results"]

items = []
for f in films:
    if not f.get("poster_path"):
        continue
    title = escape(f["title"])
    img = IMG + f["poster_path"]
    link = "https://www.themoviedb.org/movie/%d" % f["id"]
    desc = escape((f.get("overview") or "")[:200])
    items.append(f"""    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid>{link}</guid>
      <description>{desc}</description>
      <enclosure url="{img}" type="image/jpeg" length="0"/>
      <media:thumbnail url="{img}"/>
      <media:content url="{img}" medium="image"/>
    </item>""")
    if len(items) >= 15:
        break

xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>Au cinéma en ce moment</title>
    <link>https://www.themoviedb.org/movie/now-playing</link>
    <description>Films à l'affiche en France</description>
    <lastBuildDate>{formatdate()}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""
with open("feed.xml", "w", encoding="utf-8") as fh:
    fh.write(xml)
print(len(items), "films écrits")
