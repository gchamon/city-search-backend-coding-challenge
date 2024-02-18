import flask

from backend_lib import CANADA_CATALOG, query_name, filter_query_results_attributes

app = flask.Flask(__name__)


@app.route("/suggestions", methods=["GET"])
def suggest_cities_by_name():
    suggestions = query_name(catalog=CANADA_CATALOG, query=flask.request.args["q"])
    suggestions_with_filtered_attributes = filter_query_results_attributes(suggestions)
    return flask.jsonify(suggestions_with_filtered_attributes)
