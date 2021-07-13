import datetime
import string
import secrets
import sys

from flask import Flask, request, Response, redirect
from flask_sqlalchemy import SQLAlchemy

db_path = 'test.db'
db_uri = 'sqlite:///' + db_path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # This suppresses some deprecation warning
db = SQLAlchemy(app)

alphabet = string.ascii_letters + string.digits + "_"


class ShortCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(length=6))
    url = db.Column(db.String(length=256))
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


@app.route("/<shortcode>/stats", methods=["GET"])
def get_stats(shortcode):
    short_code = ShortCode.query.filter_by(short_code=shortcode).first()
    if short_code is not None:
        print(type(short_code.last_redirect), file=sys.stdout)
        data = {"created": short_code.created.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "lastRedirect": short_code.last_redirect.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "redirectCount": short_code.redirect_count
                }
        return data, 200
    else:
        return Response(status=404)


@app.route("/<shortcode>", methods=["GET"])
def get_shortcode(shortcode):
    short_code = ShortCode.query.filter_by(short_code=shortcode).first()
    if short_code is not None:
        short_code.redirect_count += 1
        short_code.last_redirect = datetime.datetime.now()
        db.session.commit()
        response = redirect(short_code.url)
        return response
    else:
        return Response(status=404)


@app.route("/shorten", methods=["POST"])
def shorten():
    try:
        url = request.json['url']
    except KeyError:
        return Response(status=400)
    try:
        sc = request.json['shortcode']

        if not is_valid_short_code(sc):
            return Response(status=412)

        short_code = ShortCode.query.filter_by(short_code=sc).all()
        if len(short_code) > 0:
            return Response(status=409)
        else:
            short_code = ShortCode(short_code=sc, url=url)

    except KeyError:
        sc = ''.join(secrets.choice(alphabet) for i in range(6))
        short_code = ShortCode(short_code=sc, url=url)

    if short_code is not None:
        db.session.add(short_code)
        db.session.commit()

    data = {"shortcode": sc}
    return data, 201


if __name__ == "__main__":
    app.run()
