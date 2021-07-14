from app.app import is_valid_short_code


def test_is_valid_short_code():
    assert is_valid_short_code("abcdef")
    assert not is_valid_short_code("abcde")
    assert not is_valid_short_code("abcde")
    assert not is_valid_short_code("abcd+f")
