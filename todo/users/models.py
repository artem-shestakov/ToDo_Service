from todo import mongo
from marshmallow import Schema, fields, post_load
from bson import ObjectId
from passlib.hash import pbkdf2_sha256
from datetime import datetime

Schema.TYPE_MAPPING[ObjectId] = fields.String


class Role(mongo.Document):
    """User's role"""
    title = mongo.StringField(required=True, unique=True)


class User(mongo.Document):
    """User model"""
    email = mongo.EmailField(required=True, unique=True)
    password = mongo.StringField(required=True)
    first_name = mongo.StringField(required=True)
    last_name = mongo.StringField(required=True)
    avatar = mongo.StringField(default=None)
    created = mongo.DateTimeField(default=datetime.now())
    is_verified = mongo.BooleanField(required=True, default=False)
    roles = mongo.ListField(mongo.ReferenceField(Role))

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
    class Meta:
        ordered = True
    id = fields.String()
    email = fields.Email(required=True)
    password = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    avatar = fields.String()
    is_verified = fields.Boolean()
    created = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
