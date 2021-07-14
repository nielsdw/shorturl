from app.app import ShortCode, app, db

db.create_all()


def test_get_shortcode():
    short_code = ShortCode(short_code="xxxxxx", url="https://www.google.com")
    db.session.add(short_code)
    db.session.commit()
    with app.test_client() as test_client:
        response = test_client.get("/xxxxxx")
        assert response.status_code == 302
        assert "https://www.google.com" == response.headers["Location"]
        response = test_client.get("/yyyyyy")
        assert response.status_code == 404
