from peewee import SqliteDatabase, Model

db = SqliteDatabase("/etc/openvpn/openvpn.db")
db.connect()


class BaseModel(Model):
    class Meta:
        database = db

