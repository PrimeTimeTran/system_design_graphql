from src import db

class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(250))
    done = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default="PENDING")
