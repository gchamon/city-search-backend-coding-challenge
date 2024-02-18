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


def filter_query_results_attributes(query_results):
    return [{"name": r["name"], "lat": r["lat"], "long": r["long"]} for r in query_results]


CANADA_CATALOG = load_catalog("data/cities_canada-usa.tsv")

if __name__ == "__main__":
    kirks = (city for city in CANADA_CATALOG if "Kirk" in city["name"])
    print(CANADA_CATALOG[0])
    print(CANADA_CATALOG[-1])
    import json

    print(json.dumps(filter_query_results_attributes(kirks), indent=2))
