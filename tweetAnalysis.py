import sys
import csv

outfile = "geotweets.csv"
# csvfile = file(outfile, "r")
tweets = []
with open(outfile, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      tweets.append(row)

print(tweets)

