# from summa.summarizer import summarize

text = """Automatische Zusammenfassung ist der Prozess zum Reduzieren eines Textdokuments mit einem
Computerprogramm, um eine Zusammenfassung zu erstellen, die die wichtigsten Punkte enthalt
des Originaldokuments. Da das Problem der Informationsuberlastung gewachsen ist, und wie
die Datenmenge hat zugenommen, hat also Interesse an der automatischen Zusammenfassung.
Technologien, die eine koharente Zusammenfassung machen konnen, berucksichtigen Variablen wie
Lange, Schreibstil und Syntax. Ein Beispiel fur die Verwendung der Zusammenfassungstechnologie
ist Suchmaschinen wie Google. Dokumentenzusammenfassung ist eine andere."""

# print(summarize(text, language='german'))

from rake_nltk import Rake

# Uses stopwords for english from NLTK, and all puntuation characters.
# r = Rake()
r = Rake(language="german")

print(r.extract_keywords_from_text(text))

r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.

print(r.get_ranked_phrases())