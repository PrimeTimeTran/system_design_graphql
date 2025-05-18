from graphene import ObjectType, String, Boolean, Field, Mutation, ID

from src import db
from src.models.enum import StatusEnum
from src.models.todo import TodoModel
from src.schema.types import Todo


class CreateTodo(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        done = Boolean()
        status = StatusEnum()

    todo = Field(lambda: Todo)

    def mutate(root, info, title, description, done=False, status="PENDING"):
        new_todo = TodoModel(
            title=title, description=description, done=done, status=status
        )
        db.session.add(new_todo)
        db.session.commit()
        return CreateTodo(todo=new_todo)


class UpdateTodo(Mutation):
    class Arguments:
        id = ID(required=True)
        title = String()
        description = String()
        done = Boolean()
        status = StatusEnum()

    todo = Field(lambda: Todo)

    def mutate(root, info, id, title=None, description=None, done=None, status=None):
        todo = TodoModel.query.get(id)
        if not todo:
            raise Exception("Todo not found")
        if title:
            todo.title = title
        if description:
            todo.description = description
        if done is not None:
            todo.done = done
        if status:
            todo.status = status
        db.session.commit()
        return UpdateTodo(todo=todo)


class DeleteTodo(Mutation):
    class Arguments:
        id = ID(required=True)

    success = String()

    def mutate(root, info, id):
        todo = TodoModel.query.get(id)
        if todo:
            db.session.delete(todo)
            db.session.commit()
            return DeleteTodo(success="Todo deleted")
        else:
            raise Exception("Todo not found")


class Mutation(ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()
