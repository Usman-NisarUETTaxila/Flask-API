from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"User {self.id} -> {self.name}"

user_args = reqparse.RequestParser()
user_args.add_argument('name',type=str,required=True,help="Name cannot be empty")

userFields = {
    'id': fields.Integer,
    'name':fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = User.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = User(name=args["name"])
        db.session.add(user)
        db.session.commit()
    
api.add_resource(Users, '/api/Users')

@app.route('/')
def home_page():
    return "<h1>API practice</h1>"


if __name__ == "__main__":
    app.run(debug=True)