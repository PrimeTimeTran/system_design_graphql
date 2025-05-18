from graphene import Schema
from flask_graphql import GraphQLView

from src import create_app
from src.schema.queries import Query
from src.schema.mutations import Mutation

app = create_app()

schema = Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True),
)

if __name__ == "__main__":
    app.run(debug=True)
