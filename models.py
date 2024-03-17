from bson import json_util
from mongoengine import connect, Document, BooleanField, StringField, ReferenceField, ListField, CASCADE

connect(db="hw_8", host="mongodb://localhost:27017")


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}

    @property
    def full_name(self):
        return self.fullname

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["_id"] = str(data["_id"])
        return json_util.dumps(data, ensure_ascii=False)


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["_id"] = str(data["_id"])
        data["author"] = self.author.full_name
        return json_util.dumps(data, ensure_ascii=False)


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(max_length=100, required=True)
    phone_number = StringField(max_length=15)
    prefer_sms = BooleanField(default=False)
    message_sent = BooleanField(default=False)
    address = StringField(max_length=200)
    meta = {"collection": "contacts"}