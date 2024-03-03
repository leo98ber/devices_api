from datetime import datetime
from mongoengine import Document, fields


class History(Document):
    host =  fields.StringField(required=True, unique=False)
    latency = fields.FloatField(null=True)
    moment = fields.DateTimeField(default=datetime.now)
    status = fields.StringField(choices=['success', 'error'])
