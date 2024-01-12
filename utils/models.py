from peewee import *
from datetime import datetime
from utils.config import MESSAGE_ARCHIVE_DURATION

database = SqliteDatabase('data/database.db')


class MessageArchive(Model):
    id = PrimaryKeyField()
    text = TextField(null=True, unique=True)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = database

    @classmethod
    def delete_expired_records(cls):
        expired_records = cls.select().where(cls.created_at < MESSAGE_ARCHIVE_DURATION)
        if expired_records:
            num_deleted = expired_records.count()
            expired_records.delete_instance()
            print(f"{num_deleted} expired records deleted.")
        else:
            print("No expired records found.")


def main():
    database.create_tables([MessageArchive])


if __name__ == '__main__':
    main()
