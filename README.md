# shorturl

This is the work that was created upon the assignment in ASSIGNMENT.txt.

It was tested on Python 3.8.

To install:

`python3.8 -m venv env`

`. env/bin/activate`

`pip install -r requirements.txt`

Create database:

`python`

`>>> from app.app import db`

`>>> db.create_all()`

This makes the endpoints available for use

`python app/app.py`

This tests all the endpoints with different data as input

`pytest`
