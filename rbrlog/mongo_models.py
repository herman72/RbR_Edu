from django.db import models
# from django_mongoengine import Document, EmbeddedDocument, fields
from mongoengine import fields, Document
from datetime import datetime


class User(Document):

    def __str__(self):
        return self.name

    # def __init__(self, name, email, ip, hpass):
    #     self.name = name
    #     self.email = email
    #     self.ip = ip
    #     self.hashed_password = hpass

    name = fields.StringField(verbose_name="Name", max_length=255, unique=True)
    email = fields.EmailField(verbose_name="Email", required=True, unique=True)
    ip = fields.StringField(verbose_name="IP", max_length=255)
    created_time = fields.DateTimeField(default=datetime.now)
    hashed_password = fields.StringField(verbose_name="PWD", required=True)


class DeviceInfo(Document):

    def __str__(self):
        return self.ip

    ip = fields.StringField(verbose_name="IP", max_length=255)
    numtry = fields.IntField(default=0)
    login_time = fields.DateTimeField(verbose_name="Login_Time", default=datetime.now)


