import json
from unittest import TestCase
from src import jsonapi


class TestBetterEncoder(TestCase):
    def test_encode_complex_number(self):
        cx = complex(1, 2)
        actual = jsonapi.dumps(cx, cls=jsonapi.BetterEncoder)
        expected = '{"real": 1.0, "imag": 2.0, "__extended_json_type__": "complex"}'
        assert actual == expected

    def test_encode_range(self):
        rg = range(1, 10, 3)
        actual = jsonapi.dumps(rg, cls=jsonapi.BetterEncoder)
        expected = '{"start": 1, "stop": 10, "step": 3, "__extended_json_type__": "range"}'
        assert actual == expected

    def test_decode_complex_number(self):
        encoded_cx = jsonapi.dumps(complex(1, 2), cls=jsonapi.BetterEncoder)
        actual = jsonapi.loads(encoded_cx, cls=jsonapi.BetterDecoder)
        expected = complex(1, 2)
        assert actual == expected

    def test_decode_range(self):
        encoded_rg = jsonapi.dumps(range(1, 10, 3), cls=jsonapi.BetterEncoder)
        actual = jsonapi.loads(encoded_rg, cls=jsonapi.BetterDecoder)
        expected = range(1, 10, 3)
        assert list(actual) == list(expected)

    def test_encode_unknown_type(self):
        obj = {"name": "John", "age": 30}
        actual = jsonapi.dumps(obj, cls=jsonapi.BetterEncoder)
        expected = '{"name": "John", "age": 30}'
        assert actual == expected

    def test_decode_unknown_type(self):
        encoded_obj = '{"name": "Alice", "city": "New York"}'
        actual = jsonapi.loads(encoded_obj, cls=jsonapi.BetterDecoder)
        expected = {"name": "Alice", "city": "New York"}
        assert actual == expected

    def test_decode_empty_json(self):
        encoded_empty = '{}'
        actual = jsonapi.loads(encoded_empty, cls=jsonapi.BetterDecoder)
        expected = {}
        assert actual == expected

    def test_decode_invalid_json(self):
        invalid_json = '{"name": "Tom", "age": 25,'
        try:
            jsonapi.loads(invalid_json, cls=jsonapi.BetterDecoder)
        except json.JSONDecodeError as e:
            assert "Expecting property name enclosed in double quotes" in str(e)