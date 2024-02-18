import flask

from backend_lib import CANADA_CATALOG, query_name, filter_query_results_attributes, EmptyQueryError

app = flask.Flask(__name__)


@app.route("/suggestions", methods=["GET"])
def suggest_cities_by_name():
    query = flask.request.args["q"]
    try:
        suggestions = query_name(catalog=CANADA_CATALOG, query=query)
        if suggestions:
            suggestions_with_filtered_attributes = filter_query_results_attributes(suggestions)
            return flask.jsonify(suggestions_with_filtered_attributes)
        else:
            return f"No matches for query '{query}'", 404
    except EmptyQueryError:
        return "Empty query q", 400
