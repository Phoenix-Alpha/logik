from flask import Flask, render_template
from strawberry.flask.views import GraphQLView

from .schemas.customer_portal import schema

app = Flask(__name__)


@app.route("/playground")
def playground() -> str:
    return render_template("graphql-playground.html")


@app.route("/voyager")
def voyager() -> str:
    return render_template("graphql-voyager.html")


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
