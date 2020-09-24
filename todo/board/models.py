from .. import mongo
from marshmallow import Schema, fields
from bson import ObjectId
from todo.auth.models import User

Schema.TYPE_MAPPING[ObjectId] = fields.String


class Board(mongo.Document):
    """Board model"""
    name = mongo.StringField(required=True)
    user = mongo.ReferenceField(User)


class BoardSchema(Schema):
    """Board marshmallow schema"""
    id = fields.String()
    name = fields.String(required=True)
    user = fields.String(required=True)

