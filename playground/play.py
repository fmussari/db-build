import sqlite_utils

db_path = 'casa'
db = sqlite_utils.Database(db_path)

print(db.schema)