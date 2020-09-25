from .. import mongo
from marshmallow import Schema, fields
from bson import ObjectId
from datetime import datetime

Schema.TYPE_MAPPING[ObjectId] = fields.String


class User(mongo.Document):
    """User model"""
    email = mongo.EmailField(required=True, unique=True)
    first_name = mongo.StringField(required=True)
    last_name = mongo.StringField(required=True)
    created = mongo.DateTimeField(default=datetime.now())


class UserSchema(Schema):
    """User marshmallow schema"""
    id = fields.String()
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created = fields.DateTime()
