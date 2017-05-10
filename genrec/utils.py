from json import JSONEncoder


class JSONEncoderObj(JSONEncoder):
    def default(self, obj):
        try:
            return obj.to_json()
        except:
            pass
        return self.default(obj)


def chunks(l, chunk_size):
    for i in range(0, len(l), chunk_size):
        yield l[i:i+chunk_size]

