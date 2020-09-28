from .. import mongo
from marshmallow import Schema, fields
from bson import ObjectId
from todo.auth.models import User

Schema.TYPE_MAPPING[ObjectId] = fields.String


class List(mongo.Document):
    title = mongo.StringField(required=True)


class ListSchema(Schema):
    id = fields.String()
    title = fields.String(required=True)


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
