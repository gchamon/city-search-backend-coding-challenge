import csv

class EmptyQueryError(Exception):
    pass

def load_catalog(catalog_filename):
    with open(catalog_filename) as catalog_fp:
        catalog = csv.DictReader(catalog_fp, delimiter="\t", quoting=csv.QUOTE_NONE)
        return list(catalog)

def query_name(catalog, query):
    if query:
        return sorted([city for city in catalog if query in city["name"]], key=lambda x: x["name"])
    else:
        raise EmptyQueryError()

if __name__ == "__main__":
    canada_catalog = load_catalog("data/cities_canada-usa.tsv")
    print(canada_catalog[0])
    print(canada_catalog[-1])
    kirks = (city for city in canada_catalog if "Kirk" in city["name"])
    import json
    print(json.dumps([{"name": k["name"], "lat": k["lat"], "long": k["long"]} for k in kirks], indent=2))


