from dataclasses import dataclass
from typing import List
import psycopg2

connection_info = {
    'database': "jellynote",
    'user': "jelly",
    'password': "j3llynote",
    'host': "localhost",
    'port': "5432"
}

conn = psycopg2.connect(**connection_info)


@dataclass(frozen=True)
class Table(object):
    name: str
    alias: str
    fields: List[str]

    def all_fields(self):
        return ', '.join(self.fields)

    def all_fields_aliased(self, alias=self.alias):
        return ', '.join(map(lambda x: alias + '.' + x, self.fields))


Users = Table('users', 'u', ['id', 'name', 'email', 'instruments', 'created_at', 'updated_at'])

tables = [Users]

# with conn.cursor() as cur:
#     cur.execute("""SELECT id, name, email, instruments, created_at, updated_at FROM users""")
#     for row in cur.fetchall():
#         print(row)
