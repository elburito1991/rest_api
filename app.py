import flask
from flask import Flask, request, jsonify, make_response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, ValidationError, EXCLUDE
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    'postgres', '', '127.0.0.1', 5432, 'db', )
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    specialisation = db.Column(db.String(50), nullable=False)

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<ID %d>' % self.id


class AuthorSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)


@app.route('/authors/<id>', methods=['GET'], strict_slashes=False)
def get_author_by_id(id):
    get_author = Authors.query.get(id)
    if not get_author:
        return flask.jsonify({'message': 'dont exist'}), 404
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({"authors": author})), 200


@app.route('/authors', methods=['GET'], strict_slashes=False)
def author_get():
    get_authors = Authors.query.all()

    if len(get_authors) == 0:
        return flask.jsonify({'message': 'not found'}), 404

    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))


@app.route('/authors', methods=['POST'])
def author_create():
    try:
        data = request.get_json()
    except BadRequest:
        return flask.jsonify({'message': 'bad json'}), 400

    if len(data) == 0:
        return flask.jsonify({'message': 'json empty'}), 400

    try:
        author_schema = AuthorSchema()
        author_schema.load(data)

        author_inst = Authors(name=data['name'], specialisation=data['specialisation'])
        author = author_inst.create()

        result = author_schema.dump(author)

        return flask.jsonify({"author": result}), 201

    except ValidationError as e:
        return flask.jsonify({'message': str(e.messages)}), 400


@app.route('/authors/<id>', methods=['PUT'], strict_slashes=False)
def update_author_by_id(id):
    try:
        data = request.get_json()

    except BadRequest:
        return flask.jsonify({'message': 'bad json'}), 400
    if len(data) == 0:
        return flask.jsonify({'message': 'json empty'}), 400

    get_author = Authors.query.get(id)

    if not get_author:
        return flask.jsonify({'message': 'dont exist'}), 404

    author_schema = AuthorSchema()

    if data.get('specialisation'):
        get_author.specialisation = data['specialisation']
    else:
        return flask.jsonify({'message': 'отсутствует поле specialisation'}), 400
    if data.get('name'):
        get_author.name = data['name']
    else:
        return flask.jsonify({'message': 'отсутствует поле name'}), 400

    try:
        author = get_author.create()
        result = author_schema.dump(author)

        return flask.jsonify({"author": result}), 201

    except ValidationError as e:
        return flask.jsonify({'message': str(e.messages)}), 400


@app.route('/authors/<id>', methods=['DELETE'], strict_slashes=False)
def delete_author_by_id(id):
    get_author = Authors.query.get(id)
    if not get_author:
        return flask.jsonify({'message': 'dont exist'}), 404
    Authors.delete(get_author)
    return flask.jsonify({'message': 'Success'}), 204


if __name__ == "__main__":
    app.run(debug=True)
