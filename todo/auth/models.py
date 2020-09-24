from .. import mongo
from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String


class User(mongo.Document):
    """User model"""
    email = mongo.StringField(required=True)
    first_name = mongo.StringField(required=True)
    last_name = mongo.StringField(required=True)


class UserSchema(Schema):
    """User marshmallow schema"""
    id = fields.String()
    email = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
