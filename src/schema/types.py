from graphene_sqlalchemy import SQLAlchemyObjectType

from src.models.todo import TodoModel


class Todo(SQLAlchemyObjectType):
    class Meta:
        model = TodoModel
