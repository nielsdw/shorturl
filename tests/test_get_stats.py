from app.app import ShortCode, app, db


def test_get_stats():
    short_code = ShortCode(short_code='xxxxxx', url='https://www.google.com')
    db.session.add(short_code)
    db.session.commit()
    with app.test_client() as test_client:
        response = test_client.get('/xxxxxx')
        # sys.stdout.write(response.data)
        assert response.status_code == 200
