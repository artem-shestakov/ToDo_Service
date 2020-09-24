from .. import mongo
from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String


class Board(mongo.Document):
    name = mongo.StringField()


class BoardSchema(Schema):
    id = fields.String()
    name = fields.String(required=True)
