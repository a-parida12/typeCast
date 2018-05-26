
# DELETE BEFORE MAKING THE REPO PUBLIC IMPORTANT!!!!!!!!
config = {}
config["consumer_key"] = "n47vnH3SEYVr343ckh4ytHopx"
config["consumer_secret"] = "BAMUGLPv82NO0KIg0sim18nZrdmmR46FnXLKWLYO26aGSNNlCs"
config["access_key"] = "2195450682-fHHCAfEmZr4mwi77esa1uMzRTTwKjwutfn9UXpf"
config["access_secret"] = "sUf5m6dB9G6XUfwXvraKxuRd2Jq14PRVhJdz0fK4W55ea"

#!/usr/bin/python


#-----------------------------------------------------------------------
# twitter-search-geo
#  - performs a search for tweets close to New Cross, London,
#    and outputs them to a CSV file.
#-----------------------------------------------------------------------

from twitter import *

import sys
import csv
import re

latitude = 48.1351  # geographical centre of search
longitude = 11.5820 # geographical centre of search
max_range = 1       # search range in kilometres
num_results = 100    # minimum results to obtain
outfile = "geotweets.csv"

twitter = Twitter(
            auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

csvfile = file(outfile, "w")
csvwriter = csv.writer(csvfile)

row = [ "user", "text", "latitude", "longitude" ]
csvwriter.writerow(row)

result_count = 0
last_id = None
while result_count <  num_results:
  query = twitter.search.tweets(q = "", geocode = "%f,%f,%dkm" % (latitude, longitude, max_range), count = 100, max_id = last_id)

  for result in query["statuses"]:
    if result["geo"]:
      user = result["user"]["screen_name"]
      text = result["text"]
      text = text.encode('ascii', 'replace')
      url = ""
      url_results = re.search("(?P<url>https?://[^\s]+)", text)
      if url_results:
        url = url_results.group("url")
      latitude = result["geo"]["coordinates"][0]
      longitude = result["geo"]["coordinates"][1]
      row = [ user, text, latitude, longitude, url ]
      csvwriter.writerow(row)
      result_count += 1
    last_id = result["id"]

  print "got %d results" % result_count

csvfile.close()

print "written to %s" % outfile