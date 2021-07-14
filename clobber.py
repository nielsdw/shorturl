from flaskr.app import db
from flaskr.app import db_path
import os

if os.path.isfile(db_path):
    print("Removing", db_path)
    os.remove(db_path)

print("Creating", db_path)
db.create_all()
