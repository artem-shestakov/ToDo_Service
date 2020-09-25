from .. import mongo
from marshmallow import Schema, fields
from bson import ObjectId
from passlib.hash import pbkdf2_sha256
from datetime import datetime

Schema.TYPE_MAPPING[ObjectId] = fields.String


class User(mongo.Document):
    """User model"""
    email = mongo.EmailField(required=True, unique=True)
    password = mongo.StringField(required=True)
    first_name = mongo.StringField(required=True)
    last_name = mongo.StringField(required=True)
    created = mongo.DateTimeField(default=datetime.now())

    @staticmethod
    def generate_password(password):
        """Generate user's password"""
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password, hash):
        """Verify user's password"""
        return pbkdf2_sha256.verify(password, hash)


class UserSchema(Schema):
    """User marshmallow schema"""
    id = fields.String()
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created = fields.DateTime()
