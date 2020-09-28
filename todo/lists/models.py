from .. import mongo
from marshmallow import Schema, fields


class List(mongo.Document):
    """List model"""
    title = mongo.StringField(required=True)


class ListSchema(Schema):
    """List schema"""
    id = fields.String()
    title = fields.String(required=True)