import csv

def load_catalog(catalog_filename):
    with open(catalog_filename) as catalog_fp:
        catalog = csv.DictReader(catalog_fp, delimiter="\t", quoting=csv.QUOTE_NONE)
        return list(catalog)

if __name__ == "__main__":
    canada_catalog = load_catalog("data/cities_canada-usa.tsv")
    print(canada_catalog[0])
    print(canada_catalog[-1])
