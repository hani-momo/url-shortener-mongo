from mongoengine import Document, StringField


class URL(Document):
    original_url = StringField(required=True)
    shortened_url = StringField(required=True)
