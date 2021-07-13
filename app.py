import sys

from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy

import datetime
import string
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

alphabet = string.ascii_letters + string.digits + "_"


class ShortCode(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	short_code = db.Column(db.String(length=6))
	created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	last_redirect = db.Column(db.DateTime, nullable=True)
	redirect_count = db.Column(db.Integer, default=0)


def is_valid_short_code(short_code):
	if len(short_code) != 6:
		return False
	for char in short_code:
		if char not in alphabet:
			return False
	return True


@app.route("/shorten", methods=["POST"])
def shorten():
	try:
		request.json['url']
	except KeyError:
		return Response(status=400)
	try:
		sc = request.json['shortcode']
		if not is_valid_short_code(sc):
			return Response(status=412)
		short_code = ShortCode.query.filter_by(short_code=sc).all()
		print(short_code, file=sys.stdout)
		if len(short_code) > 0:
			return Response(status=409)
		else:
			short_code = ShortCode(short_code=sc)
	except KeyError:
		sc = ''.join(secrets.choice(alphabet) for i in range(6))
		short_code = ShortCode(short_code=sc)

	if short_code is not None:
		db.session.add(short_code)
		db.session.commit()

	print("SC", sc, file=sys.stdout)
	data = {"shortcode": sc}
	return data, 201


if __name__ == "__main__":
	app.run()
