import wikipedia
import requests
import re

_DATA_PATH = "data/"
_COMPOSERSFILE = "composers.csv"
_english_url = re.compile('<a href="//en.wikipedia.org/wiki/.+" title="(.+) — .+" lang="en" hreflang="en">English</a>')
_lang_indexes = {'ru': 0, 'en': 1}

def load_composers():
    with open(_DATA_PATH + _COMPOSERSFILE, "r", encoding="utf-8") as filestream:
        composers = [row.split("\t") for row in filestream.read().split("\n")]
    return composers

'''Use only once'''
def save_english_names():
    authors = []
    wikipedia.set_lang("ru")
    with open(_DATA_PATH + "composers_ru.txt", "r", encoding="utf-8") as filestream:
        composers = filestream.read().split("\n")

    for author in composers:
        print("Finding english url for %s..." % author)
        page = wikipedia.page(author)
        authors.append(author + "\t" + get_english_analogue(page.url))

    with open(_DATA_PATH + _COMPOSERSFILE, "w", encoding="utf-8") as filestream:
        filestream.write("\n".join(authors))

def get_english_analogue(url):
    r = requests.get(url)
    assert r.status_code == 200
    regUrl = _english_url.search(r.text)
    if regUrl:
        return regUrl.group(1).replace("_", " ")
    else:
        print("No url for english page has been found")

def find_references(author, composers):
    page = wikipedia.page(author)
    links = page.links
    references = []
    for link in links:
        link = link.replace(",", "")
        if link in composers:
            references.append(link)
    return references


def get_connections_by_lang(lang="ru"):
    wikipedia.set_lang(lang)
    connections = []
    composers = [comp[_lang_indexes[lang]] for comp in _COMPOSERS_LIST]
    for composer in composers:
        print("Finding references for %s..." % composer)
        references = find_references(composer, composers)
        if references:
            for ref in references:
                connections.append(composer + "\t" + ref)
    with open(_DATA_PATH + "%s_connections.csv" % lang, "w", encoding="utf-8") as filestream:
        filestream.write("\n".join(connections))
    return connections

def load_connections(lang):
    with open(_DATA_PATH + "%s_connections.csv" % lang, "r", encoding="utf-8") as filestream:
        connections = [row.split("\t") for row in filestream.read().split("\n")]
    return connections

def save_connections():
    connections = []
    for lang in _lang_indexes.keys():
        connections += get_connections_by_lang(lang)
    with open(_DATA_PATH + "all_connections.csv", "w", encoding="utf-8") as filestream:
        filestream.write("\n".join(connections))

def en_on_ru_connections(_COMPOSERS_LIST):
    connections = load_connections("en")
    composers_list = dict([(v,k) for k,v in _COMPOSERS_LIST])
    ru_on_en_connections = [composers_list[source] + "\t" + composers_list[target] for source, target in connections]
    with open(_DATA_PATH + "en(ru)_connections.csv", "w", encoding="utf-8") as filestream:
        filestream.write("\n".join(ru_on_en_connections))

if __name__ == "__main__":
    _COMPOSERS_LIST = load_composers()
    save_connections()
    en_on_ru_connections(_COMPOSERS_LIST)