from sqlalchemy import or_

from graphene import (
    ID,
    List,
    Field,
    String,
    ObjectType,
)

from src.schema.types import Todo
from src.models.todo import TodoModel


class Query(ObjectType):
    all_todos = List(Todo)
    todo = Field(Todo, id=ID(required=True))
    todos_by_title = List(Todo, title=String(required=True))
    todos_search = List(Todo, term=String(required=True))

    def resolve_all_todos(root, info):
        return TodoModel.query.all()

    def resolve_todo(root, info, id):
        return TodoModel.query.get(id)

    def resolve_todos_by_title(root, info, title):
        search = f"%{title}%"
        return TodoModel.query.filter(TodoModel.title.ilike(search)).all()

    def resolve_todos_search(root, info, term):
        search = f"%{term}%"
        return TodoModel.query.filter(
            or_(TodoModel.title.ilike(search), TodoModel.description.ilike(search))
        ).all()
