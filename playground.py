# from summa.summarizer import summarize
import json

from eventregistry import *
er = EventRegistry(apiKey = 'ab40eb06-3900-4689-a369-b4098f4e49ef')


text = """
Mit Beginn der Tail Emission von 157.788 XMR p. a. ab ca. Mitte 2022 bei einer dann emittierten Geldmenge von 18,132 Millionen XMR liegt das nominale Geldmengenwachstum bei anfänglich 0,87 % p. a., wird in der Folge aufgrund der dauernd steigenden Gesamtzahl emittierten Geldes aber kontinuierlich fallen und langfristig gegen 0 % konvergieren.

Da benutzerbedingt immer wieder Moneros verloren gehen werden (Verlust privater Schlüssel, Hardware-Defekte, fehlende Backups), könnte sich durch den Mechanismus der Tail Emission langfristig ein ungefähres Gleichgewicht zwischen der Rate verlorener und neu erzeugter Coins einstellen. Das bedeutet, dass Monero trotz der dauerhaften Erzeugung neuer Währungseinheiten langfristig als Währung mit stabiler Geldmenge angesehen werden könnte.
Anonymität und Datenschutz
"""


analytics = Analytics(er)
ann = analytics.annotate(text)
annotations = []
parsed_json = json.loads(json.dumps(ann))
for annotation in parsed_json[u'annotations']:
  annotations.append(annotation[u'title'])

print(annotations)

# # print(summarize(text, language='german'))

# from rake_nltk import Rake

# # Uses stopwords for english from NLTK, and all puntuation characters.
# # r = Rake()
# r = Rake(language="german")

# print(r.extract_keywords_from_text(text))

# r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.

# print(r.get_ranked_phrases())