from graphene import (
    ID,
    List,
    Field,
    ObjectType,
)

from src.schema.types import Todo
from src.models.todo import TodoModel


class Query(ObjectType):
    all_todos = List(Todo)
    todo = Field(Todo, id=ID(required=True))

    def resolve_all_todos(root, info):
        return TodoModel.query.all()

    def resolve_todo(root, info, id):
        return TodoModel.query.get(id)
