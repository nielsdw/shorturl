from app.app import ShortCode, app, db
db.drop_all()
db.create_all()


def test_shorten():
    with app.test_client() as test_client:
        response = test_client.post('/shorten', json={"shortcode": "abcdef"})
        assert response.status_code == 400

        response = test_client.post('/shorten', json={"shortcode": "abcdef", "url": "https://foo.bar"})
        assert response.status_code == 201
        assert response.json["shortcode"] == "abcdef"

        response = test_client.post('/shorten', json={"shortcode": "abcd+f", "url": "https://foo.bar"})
        assert response.status_code == 412

        response = test_client.post('/shorten', json={"shortcode": "abcdef", "url": "https://foo.bar"})
        assert response.status_code == 409

        response = test_client.post('/shorten', json={"url": "https://foo.bar"})
        assert response.status_code == 201

