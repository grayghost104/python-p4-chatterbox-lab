from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)



@app.route('/messages', methods = ["GET", "POST"])
def messages():
    method = request.method
    if method == "GET":
        all_mess = Message.query.order_by(Message.created_at.asc()).all()
        ever=[mess.to_dict() for mess in all_mess]
        return jsonify(ever)
    elif method == "POST":
        try:
            data = request.get_json()
            editing = Message(
                body = data["body"],
                username = data["username"]
            )
            db.session.add(editing)
            db.session.commit()
            return jsonify(editing.to_dict())
        except Exception as e:
            print(e)
            return {
                "Error": "Please input all values"
            },400

@app.route('/messages/<int:id>', methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    method = request.method
    messag = Message.query.filter(Message.id == id).first()
    if messag:
        if method == "GET":
            return messag.to_dict()
        elif method == "PATCH":
            try:
                data = request.get_json()
                for key in data:
                    setattr(messag,key,data[key])
                db.session.add(messag)
                db.session.commit()
                return jsonify(messag.to_dict()),200
            except Exception as e :
                print(e)
                return {
                    "error"
                },400
        elif method == "DELETE":
            db.session.delete(messag)
            db.session.commit()
            return {}

if __name__ == '__main__':
    app.run(port=5555)
