from django.db import models
# from django_mongoengine import Document, EmbeddedDocument, fields
from mongoengine import fields, Document
from datetime import datetime


class User(Document):

    def __str__(self):
        return self.name_user

    name_user = fields.StringField(verbose_name="Name", max_length=255)
    email_user =fields.EmailField(verbose_name="Email", required=True)
    ip_user = fields.StringField(verbose_name="IP", max_length=255)
    created_time = fields.DateTimeField(default=datetime.now)
    pasword_user = fields.StringField(verbose_name="PWD", required=True)

