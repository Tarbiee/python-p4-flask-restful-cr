#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Newsletters(Resource):
    def get(self):
        newsletters=[]
        for newsletter in Newsletter.query.all():
            newsletter_dict = newsletter.to_dict()
            newsletters.append(newsletter_dict)
        response = make_response(
            jsonify(newsletters),200,
        )
        return response
    
    def post(self):
        data = request.get_json()
        newsletter = Newsletter(
            title = data['title'],
            body=data['body']
        )
        db.session.add(newsletter)
        db.session.commit()
        return make_response(newsletter.to_dict(), 201,)
    
class NewslettersByID(Resource):
    def get(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        newsletter_dict = newsletter.to_dict()
        response = make_response(
            jsonify(newsletter_dict),200,
        )
        return response


api.add_resource(Newsletters, '/newsletters')
api.add_resource(NewslettersByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
