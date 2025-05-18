from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Boolean, Field, List, Mutation, Schema, ID, Enum
from graphene_sqlalchemy import SQLAlchemyObjectType
import os

# Initialize Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(250))
    done = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='PENDING')

# 🚀 Create database within application context
with app.app_context():
    db.create_all()

# GraphQL Schema
class StatusEnum(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class Todo(SQLAlchemyObjectType):
    class Meta:
        model = TodoModel

class CreateTodo(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        done = Boolean()
        status = StatusEnum()

    todo = Field(lambda: Todo)

    def mutate(root, info, title, description, done=False, status='PENDING'):
        new_todo = TodoModel(title=title, description=description, done=done, status=status)
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
            raise Exception('Todo not found')
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
            raise Exception('Todo not found')

class Query(ObjectType):
    all_todos = List(Todo)
    todo = Field(Todo, id=ID(required=True))

    def resolve_all_todos(root, info):
        return TodoModel.query.all()

    def resolve_todo(root, info, id):
        return TodoModel.query.get(id)

class Mutation(ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

schema = Schema(query=Query, mutation=Mutation)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True)
