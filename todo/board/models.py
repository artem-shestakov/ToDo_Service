from .. import mongo
from marshmallow import Schema, fields
from bson import ObjectId
from todo.users.models import User
from todo.lists.models import List

Schema.TYPE_MAPPING[ObjectId] = fields.String


class Board(mongo.Document):
    """Board model"""
    title = mongo.StringField(required=True)
    user = mongo.ReferenceField(User)
    lists = mongo.ListField(mongo.ReferenceField(List))


class BoardSchema(Schema):
    """Board marshmallow schema"""
    id = fields.String()
    title = fields.String(required=True)
    user = fields.Mapping()
    lists = fields.Mapping()
