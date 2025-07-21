from app import app, db, UserModel

with app.app_context():
    print(UserModel.query.all())