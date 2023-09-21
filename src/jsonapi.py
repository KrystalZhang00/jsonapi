import json


class BetterEncoder(json.JSONEncoder):
    def default(self, obj):
        name = type(obj).__name__
        try:
            encoder_func = getattr(self, f"encode_{name}")
        except AttributeError:
            super().default(obj)
        else:
            encoded = encoder_func(obj)
            encoded["__extended_json_type__"] = name
            return encoded

    def encode_complex(self, obj):
        return {"real": obj.real, "imag": obj.imag}

    def encode_range(self, obj):
        return {"start": obj.start, "stop": obj.stop, "step": obj.step}


class BetterDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        kwargs["object_hook"] = self.object_hook
        super().__init__(**kwargs)

    def object_hook(self, obj):
        try:
            name = obj.get("__extended_json_type__")
            decoder_func = getattr(self, f"decode_{name}")
        except (KeyError, AttributeError):
            return obj
        else:
            return decoder_func(obj)

    def decode_complex(self, obj):
        return complex(obj["real"], obj["imag"])

    def decode_range(self, obj):
        return range(obj["start"], obj["stop"], obj["step"])


def dumps(data, cls=BetterEncoder):
    return json.dumps(data, cls=cls)


def loads(data, cls=BetterDecoder):
    return json.loads(data, cls=cls)
