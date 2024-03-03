from mongoengine import Document, fields


class Latency(Document):
    host =  fields.StringField(required=True, unique=True)
    latency = fields.FloatField(null=True)
    # moment = fields.DateTimeField(default=datetime.now)
    status = fields.StringField(choices=['success', 'error'])
